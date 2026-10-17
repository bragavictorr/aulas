from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.validators import RegexValidator
from .models import UserProfile, HiringRequest, Project, ProjectComment, PartnershipProposal, PartnershipMessage

class CustomUserCreationForm(UserCreationForm):
    username = forms.CharField(
        label="Usuário",
        max_length=150,
        validators=[
            RegexValidator(
                regex=r'^[a-zA-Z0-9_]+$',
                message='O nome de usuário deve conter apenas letras, números e sublinhados.'
            )
        ],
        help_text='Obrigatório. Apenas letras, números e sublinhado (_).'
    )
    
    email = forms.EmailField(required=True, label="E-mail")

    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email')


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('avatar', 'especialidade', 'bio', 'portfolio_url', 'location', 'available_for_hire')
        widgets = {
            'avatar': forms.FileInput(attrs={
                'class': 'avatar-file-input',
                'id': 'avatarFileInput',
                'accept': 'image/*'
            }),
            'especialidade': forms.TextInput(attrs={
                'class': 'form-control-art',
                'placeholder': 'Ex: Animação 3D, VFX Shaders, Motion 2D'
            }),
            'bio': forms.Textarea(attrs={
                'class': 'form-control-art',
                'rows': 3,
                'placeholder': 'Escreva sobre suas técnicas, ferramentas (Blender, Cinema 4D, After Effects...) e experiência.'
            }),
            'portfolio_url': forms.URLInput(attrs={
                'class': 'form-control-art',
                'placeholder': 'https://github.com/seunome ou https://behance.net/seunome'
            }),
            'location': forms.TextInput(attrs={
                'class': 'form-control-art',
                'placeholder': 'Ex: São Paulo, Brasil / Remoto'
            }),
            'available_for_hire': forms.CheckboxInput(attrs={
                'class': 'checkbox-art'
            }),
        }
        labels = {
            'avatar': 'Foto de Perfil (Avatar)',
            'especialidade': 'Especialidade Profissional',
            'bio': 'Biografia Curta',
            'portfolio_url': 'Link de Portfólio / GitHub / Behance',
            'location': 'Localização',
            'available_for_hire': 'Disponível para novos projetos e contratações',
        }


class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=60, required=False, label="Nome Completo", widget=forms.TextInput(attrs={'class': 'form-control-art', 'placeholder': 'Seu Nome'}))
    email = forms.EmailField(required=True, label="E-mail", widget=forms.EmailInput(attrs={'class': 'form-control-art'}))

    class Meta:
        model = User
        fields = ('first_name', 'email')


class HiringRequestForm(forms.ModelForm):
    class Meta:
        model = HiringRequest
        fields = ('client_name', 'client_email', 'project_title', 'budget', 'message')
        widgets = {
            'client_name': forms.TextInput(attrs={
                'class': 'form-control-art',
                'placeholder': 'Seu Nome Completo ou Empresa',
                'required': 'required'
            }),
            'client_email': forms.EmailInput(attrs={
                'class': 'form-control-art',
                'placeholder': 'seuemail@exemplo.com',
                'required': 'required'
            }),
            'project_title': forms.TextInput(attrs={
                'class': 'form-control-art',
                'placeholder': 'Ex: Abertura 3D para YouTube / Loop VFX',
                'required': 'required'
            }),
            'budget': forms.TextInput(attrs={
                'class': 'form-control-art',
                'placeholder': 'Ex: R$ 1.500 - R$ 3.000 / A combinar'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control-art',
                'rows': 4,
                'placeholder': 'Descreva os objetivos do projeto, prazos desejados, formato e referências visuais.',
                'required': 'required'
            }),
        }
        labels = {
            'client_name': 'Seu Nome / Empresa',
            'client_email': 'E-mail para Retorno',
            'project_title': 'Assunto / Nome do Projeto',
            'budget': 'Orçamento Estimado (Opcional)',
            'message': 'Mensagem e Detalhes da Proposta',
        }


class ProjectForm(forms.ModelForm):
    PREVIEW_STYLE_CHOICES = [
        ('preview-cyber', 'Cyberpunk Neon (Ciano & Azul)'),
        ('preview-retro', 'Vaporwave Retrô (Magenta & Roxo)'),
        ('preview-vfx', 'VFX Shaders (Âmbar & Dourado)'),
        ('preview-intro', 'Tipografia Cinética (Verde Neon)'),
        ('preview-cinema', 'Cinema & TV (Púrpura Cósmica)'),
        ('preview-mecha', '3D Mecha (Azul High-Tech)'),
    ]

    preview_style = forms.ChoiceField(
        choices=PREVIEW_STYLE_CHOICES,
        required=False,
        initial='preview-cyber',
        widget=forms.Select(attrs={'class': 'form-control-art'}),
        label="Estilo Visual do Card"
    )

    class Meta:
        model = Project
        fields = ('title', 'category', 'price', 'duration', 'preview_style', 'thumbnail', 'video_demo', 'description')
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control-art',
                'placeholder': 'Ex: Animação Futurista Neon / Loop Cyberpunk',
                'required': 'required'
            }),
            'category': forms.Select(attrs={'class': 'form-control-art'}),
            'price': forms.NumberInput(attrs={
                'class': 'form-control-art',
                'placeholder': 'Ex: 49.90',
                'step': '0.50'
            }),
            'duration': forms.TextInput(attrs={
                'class': 'form-control-art',
                'placeholder': 'Ex: 0:15, 0:30, 0:45 ou Loop'
            }),
            'thumbnail': forms.FileInput(attrs={
                'class': 'avatar-file-input',
                'id': 'projectThumbnailInput',
                'accept': 'image/*'
            }),
            'video_demo': forms.FileInput(attrs={
                'class': 'avatar-file-input',
                'id': 'projectVideoInput',
                'accept': 'video/mp4,video/webm,video/ogg,video/quicktime,video/*,image/gif'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control-art',
                'rows': 3,
                'placeholder': 'Conte sobre as ferramentas usadas (Blender, After Effects, Cinema 4D, Houdini...), tempo de render e conceito.'
            }),
        }
        labels = {
            'title': 'Título do Projeto',
            'category': 'Categoria de Motion',
            'price': 'Preço do Modelo 3D / Asset (R$)',
            'duration': 'Duração da Animação',
            'thumbnail': 'Capa / Thumbnail (Opcional)',
            'video_demo': 'Arquivo de Vídeo Motion (MP4, WebM, MOV, GIF)',
            'description': 'Descrição do Projeto',
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['price'].required = False
        self.fields['duration'].required = False
        self.fields['preview_style'].required = False

    def clean_price(self):
        price = self.cleaned_data.get('price')
        if price is None:
            return 49.90
        return price

    def clean_duration(self):
        duration = self.cleaned_data.get('duration')
        if not duration:
            return '0:30'
        return duration

    def clean_preview_style(self):
        style = self.cleaned_data.get('preview_style')
        if not style:
            return 'preview-cyber'
        return style



class ProjectCommentForm(forms.ModelForm):
    class Meta:
        model = ProjectComment
        fields = ('text',)
        widgets = {
            'text': forms.Textarea(attrs={
                'class': 'form-control-art comment-input',
                'rows': 2,
                'placeholder': 'Deixe um comentário sobre esta arte, feedback ou dúvidas sobre o modelo...',
                'required': 'required'
            })
        }
        labels = {
            'text': ''
        }


class PartnershipProposalForm(forms.ModelForm):
    class Meta:
        model = PartnershipProposal
        fields = ('title', 'roles', 'message')
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control-art',
                'placeholder': 'Ex: Animação Curta Metragem / Co-criação de Clipe',
                'required': 'required'
            }),
            'roles': forms.TextInput(attrs={
                'class': 'form-control-art',
                'placeholder': 'Ex: Eu faço Modelagem 3D & Você faz Texturização e Animação'
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control-art',
                'rows': 4,
                'placeholder': 'Descreva sua ideia de colaboração, referências visuais e como vocês podem somar técnicas.',
                'required': 'required'
            })
        }
        labels = {
            'title': 'Ideia / Nome do Projeto Conjunto',
            'roles': 'Divisão de Papéis / Habilidades',
            'message': 'Mensagem Inicial de Parceria'
        }


class PartnershipMessageForm(forms.ModelForm):
    class Meta:
        model = PartnershipMessage
        fields = ('text',)
        widgets = {
            'text': forms.TextInput(attrs={
                'class': 'form-control-art chat-input-field',
                'placeholder': 'Escreva uma mensagem para o artista...',
                'required': 'required',
                'autocomplete': 'off'
            })
        }
        labels = {
            'text': ''
        }