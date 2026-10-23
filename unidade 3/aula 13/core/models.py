from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import uuid

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    avatar = models.ImageField(upload_to='avatars/', blank=True, null=True, verbose_name="Foto de Perfil")
    cover_image = models.ImageField(upload_to='covers/', blank=True, null=True, verbose_name="Capa / Banner do Perfil")
    bio = models.TextField(blank=True, max_length=500, verbose_name="Biografia")
    portfolio_url = models.URLField(blank=True, max_length=250, verbose_name="Link de Portfólio / GitHub")
    especialidade = models.CharField(
        max_length=100, 
        blank=True, 
        verbose_name="Especialidade Profissional",
        help_text="Ex: Animação 3D, Motion 2D, VFX & Shaders, Tipografia Cinética"
    )
    location = models.CharField(max_length=100, blank=True, verbose_name="Localização", default="Brasil")
    available_for_hire = models.BooleanField(default=True, verbose_name="Disponível para contratação")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Perfil de {self.user.username}"

    @property
    def avatar_url(self):
        if self.avatar and hasattr(self.avatar, 'url'):
            return self.avatar.url
        return None


class Project(models.Model):
    CATEGORY_CHOICES = [
        ('3d', 'Animação 3D'),
        ('2d', 'Motion 2D & Loops'),
        ('vfx', 'VFX & Efeitos'),
        ('kinetic', 'Tipografia Cinética'),
        ('cinema', 'Cinema & TV'),
    ]

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projects')
    title = models.CharField(max_length=150, verbose_name="Título do Projeto")
    description = models.TextField(blank=True, verbose_name="Descrição do Projeto")
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default='3d', verbose_name="Categoria")
    preview_style = models.CharField(max_length=50, default='preview-cyber', verbose_name="Estilo do Preview")
    thumbnail = models.ImageField(upload_to='projects/', blank=True, null=True, verbose_name="Capa / Thumbnail do Projeto")
    video_demo = models.FileField(upload_to='project_videos/', blank=True, null=True, verbose_name="Arquivo de Vídeo/Animação")
    duration = models.CharField(max_length=20, default='0:30', verbose_name="Duração do Vídeo / Loop")
    likes = models.ManyToManyField(User, related_name='liked_projects', blank=True, verbose_name="Utilizadores que Curtiram")
    likes_count = models.PositiveIntegerField(default=0, verbose_name="Contagem Base de Curtidas")
    saved_by = models.ManyToManyField(User, related_name='saved_projects', blank=True, verbose_name="Utilizadores que Salvaram")
    views_count = models.PositiveIntegerField(default=0, verbose_name="Visualizações")
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0.00, blank=True, null=True, verbose_name="Preço do Modelo/Asset (R$)")
    is_for_sale = models.BooleanField(default=False, verbose_name="Disponível para Venda")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.title} por @{self.author.username}"

    @property
    def total_likes(self):
        return self.likes.count()

    @property
    def total_saves(self):
        return self.saved_by.count()

    @property
    def is_video_gif(self):
        if self.video_demo and self.video_demo.name:
            return self.video_demo.name.lower().endswith('.gif')
        return False


class ProjectComment(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='comments', verbose_name="Projeto")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='project_comments', verbose_name="Autor do Comentário")
    text = models.TextField(max_length=1000, verbose_name="Comentário")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data de Envio")

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Comentário de @{self.author.username} em {self.project.title}"


class ProjectPurchase(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='purchases', verbose_name="Projeto / Modelo 3D")
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='purchased_projects', verbose_name="Comprador")
    price_paid = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Valor Pago (R$)")
    license_key = models.CharField(max_length=64, blank=True, verbose_name="Chave de Licença")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data da Compra")

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.license_key:
            self.license_key = f"ARTFLOW-{uuid.uuid4().hex[:12].upper()}"
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Compra #{self.id}: @{self.buyer.username} adquiriu '{self.project.title}'"


class HiringRequest(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pendente'),
        ('contacted', 'Em Negociação'),
        ('completed', 'Concluído'),
        ('declined', 'Recusado'),
    ]

    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_proposals', verbose_name="Profissional a Contratar")
    sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='sent_proposals', verbose_name="Utilizador Solicitante")
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, blank=True, related_name='proposals', verbose_name="Projeto Relacionado")
    client_name = models.CharField(max_length=120, verbose_name="Seu Nome / Empresa")
    client_email = models.EmailField(verbose_name="E-mail de Retorno")
    project_title = models.CharField(max_length=160, verbose_name="Assunto / Nome do Projeto")
    budget = models.CharField(max_length=80, blank=True, verbose_name="Orçamento Estimado")
    message = models.TextField(verbose_name="Detalhes da Proposta de Serviço")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Status")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data de Envio")

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Proposta de {self.client_name} para @{self.creator.username} ({self.project_title})"


class PartnershipProposal(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pendente'),
        ('accepted', 'Parceria Aceita'),
        ('declined', 'Recusada'),
    ]

    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_partnerships', verbose_name="Artista Proponente")
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_partnerships', verbose_name="Artista Convidado")
    project = models.ForeignKey(Project, on_delete=models.SET_NULL, null=True, blank=True, related_name='partnerships', verbose_name="Projeto de Referência (Opcional)")
    title = models.CharField(max_length=160, verbose_name="Ideia / Título do Projeto Conjunto")
    roles = models.CharField(max_length=160, blank=True, verbose_name="Divisão de Papéis (ex: 3D + Trilha Sonora)")
    message = models.TextField(verbose_name="Proposta Inicial de Parceria")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending', verbose_name="Status da Parceria")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data de Criação")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated_at']

    def __str__(self):
        return f"Parceria '{self.title}' (@{self.sender.username} & @{self.receiver.username})"


class PartnershipMessage(models.Model):
    partnership = models.ForeignKey(PartnershipProposal, on_delete=models.CASCADE, related_name='messages', verbose_name="Parceria")
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='partnership_messages', verbose_name="Remetente")
    text = models.TextField(verbose_name="Mensagem")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Enviada em")

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f"Mensagem de @{self.sender.username} na parceria #{self.partnership.id}"


class UserSuggestion(models.Model):
    SUGGESTION_TYPES = [
        ('idea', 'Nova Ideia / Funcionalidade'),
        ('improvement', 'Melhoria Visual ou UX'),
        ('bug', 'Relato de Problema / Bug'),
        ('other', 'Outra Sugestão'),
    ]

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='suggestions', verbose_name="Usuário")
    name = models.CharField(max_length=120, blank=True, verbose_name="Nome")
    email = models.EmailField(blank=True, verbose_name="E-mail de Contato")
    suggestion_type = models.CharField(max_length=20, choices=SUGGESTION_TYPES, default='idea', verbose_name="Categoria")
    title = models.CharField(max_length=160, verbose_name="Título da Sugestão")
    message = models.TextField(verbose_name="Detalhes da Sugestão")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data de Envio")

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        user_str = f"@{self.user.username}" if self.user else (self.name or "Anônimo")
        return f"[{self.get_suggestion_type_display()}] {self.title} por {user_str}"


class UserFollow(models.Model):
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name='following_relations', verbose_name="Seguidor")
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name='followers_relations', verbose_name="Criador Seguido")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Seguindo desde")

    class Meta:
        unique_together = ('follower', 'following')
        ordering = ['-created_at']

    def __str__(self):
        return f"@{self.follower.username} segue @{self.following.username}"


class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('follow', 'Novo Seguidor'),
        ('like', 'Curtida'),
        ('comment', 'Comentário'),
        ('partnership', 'Parceria'),
        ('sale', 'Venda'),
    ]

    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications', verbose_name="Destinatário")
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_notifications', verbose_name="Remetente")
    notification_type = models.CharField(max_length=20, choices=NOTIFICATION_TYPES, default='follow', verbose_name="Tipo")
    title = models.CharField(max_length=200, verbose_name="Título")
    message = models.TextField(verbose_name="Mensagem")
    link = models.CharField(max_length=255, blank=True, verbose_name="Link de Destino")
    is_read = models.BooleanField(default=False, verbose_name="Lida")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Data de Notificação")

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Notificação para @{self.recipient.username}: {self.title}"


# Signal para criação automática do UserProfile quando um User for cadastrado
@receiver(post_save, sender=User)
def create_or_update_user_profile(sender, instance, created, **kwargs):
    if created:
        UserProfile.objects.create(user=instance)
    else:
        if hasattr(instance, 'profile'):
            instance.profile.save()
        else:
            UserProfile.objects.create(user=instance)
