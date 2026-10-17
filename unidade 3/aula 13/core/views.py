from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.db import transaction
from django.db.models import Q
from django.http import JsonResponse

from .forms import (
    CustomUserCreationForm, UserProfileForm, UserUpdateForm,
    HiringRequestForm, ProjectForm, ProjectCommentForm,
    PartnershipProposalForm, PartnershipMessageForm
)
from .models import (
    UserProfile, Project, HiringRequest, ProjectComment, ProjectPurchase,
    PartnershipProposal, PartnershipMessage
)


def landing_page(request):
    featured_projects = Project.objects.all().select_related('author__profile').order_by('-likes_count', '-created_at')[:6]
    motion_of_the_day = featured_projects.first() if featured_projects.exists() else None
    
    total_projects = Project.objects.count()
    total_creators = User.objects.count()
    
    # Calcular contagem estimada de visualizações e curtidas totais
    views_sum = sum(Project.objects.values_list('views_count', flat=True)) or 0
    likes_sum = sum(Project.objects.values_list('likes_count', flat=True)) or 0
    total_views = max(views_sum + likes_sum * 4, 3420)
    
    popular_tags = [
        {'name': 'Blender 3D', 'icon': '🎨'},
        {'name': 'After Effects', 'icon': '⚡'},
        {'name': 'Cinema 4D', 'icon': '💎'},
        {'name': 'Unreal Engine', 'icon': '🚀'},
        {'name': 'Tipografia Cinética', 'icon': '✍️'},
        {'name': 'VFX & Shaders', 'icon': '🔥'},
    ]

    return render(request, 'base.html', {
        'featured_projects': featured_projects,
        'motion_of_the_day': motion_of_the_day,
        'total_projects': max(total_projects, 15),
        'total_creators': max(total_creators, 8),
        'total_views': total_views,
        'popular_tags': popular_tags,
    })


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            messages.success(request, f"Bem-vindo de volta ao ArtFlow, @{user.username}!")
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})


def cadastro_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Garante a criação imediata do perfil
            UserProfile.objects.get_or_create(user=user)
            login(request, user)
            messages.success(request, f"Conta criada com sucesso! Boas-vindas, @{user.username}!")
            return redirect('home')
    else:
        form = CustomUserCreationForm()
    return render(request, 'cadastro.html', {'form': form})


@login_required(login_url='login')
def home_feed(request):
    projects = Project.objects.all().select_related('author__profile')
    total_projects = projects.count()
    total_users = User.objects.count()
    total_creators = User.objects.filter(projects__isnull=False).distinct().count()
    hiring_form = HiringRequestForm()
    project_form = ProjectForm()

    return render(request, 'home.html', {
        'projects': projects,
        'total_projects': total_projects,
        'total_users': total_users,
        'total_creators': total_creators,
        'hiring_form': hiring_form,
        'project_form': project_form,
    })


@login_required(login_url='login')
def profile_view(request, username):
    """
    Exibe o perfil próprio ou de outro usuário.
    Se for o próprio perfil:
    - Exibe portfólio próprio
    - Exibe projetos salvos de outros criadores
    - Exibe projetos curtidos
    - Exibe propostas de parcerias e mensagens entre artistas
    - Exibe propostas de contratação comercial recebidas
    - Permite editar dados e avatar
    Se for outro artista:
    - Exibe portfólio público
    - Botão de contratação comercial
    - Botão de propor parceria / colaboração em projetos conjuntos
    """
    target_user = get_object_or_404(User, username=username)
    profile, _ = UserProfile.objects.get_or_create(user=target_user)
    
    is_own_profile = (request.user == target_user)
    projects = Project.objects.filter(author=target_user)

    user_form = None
    profile_form = None
    received_proposals = None
    saved_projects = []
    liked_projects = []
    partnerships = []
    partnership_message_form = None

    if is_own_profile:
        received_proposals = HiringRequest.objects.filter(creator=target_user)
        saved_projects = target_user.saved_projects.all().select_related('author__profile')
        liked_projects = target_user.liked_projects.all().select_related('author__profile')
        partnerships = PartnershipProposal.objects.filter(
            Q(sender=target_user) | Q(receiver=target_user)
        ).select_related('sender__profile', 'receiver__profile', 'project').prefetch_related('messages__sender__profile').distinct()
        partnership_message_form = PartnershipMessageForm()
        
        if request.method == 'POST':
            # Atualização do perfil e foto de avatar
            user_form = UserUpdateForm(request.POST, instance=target_user)
            profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)

            if user_form.is_valid() and profile_form.is_valid():
                with transaction.atomic():
                    user_form.save()
                    profile_form.save()
                messages.success(request, "Seu perfil e avatar foram atualizados com sucesso!")
                return redirect('profile', username=target_user.username)
            else:
                messages.error(request, "Por favor, corrija os erros no formulário.")
        else:
            user_form = UserUpdateForm(instance=target_user)
            profile_form = UserProfileForm(instance=profile)

    hiring_form = HiringRequestForm()
    partnership_form = PartnershipProposalForm()
    project_form = ProjectForm()

    context = {
        'target_user': target_user,
        'profile': profile,
        'is_own_profile': is_own_profile,
        'projects': projects,
        'saved_projects': saved_projects,
        'liked_projects': liked_projects,
        'partnerships': partnerships,
        'user_form': user_form,
        'profile_form': profile_form,
        'received_proposals': received_proposals,
        'hiring_form': hiring_form,
        'partnership_form': partnership_form,
        'partnership_message_form': partnership_message_form,
        'project_form': project_form,
    }
    return render(request, 'profile.html', context)


@login_required(login_url='login')
def add_project_view(request):
    """
    Publica um novo projeto de motion design associado ao utilizador logado.
    """
    if request.method == 'POST':
        form = ProjectForm(request.POST, request.FILES)
        if form.is_valid():
            project = form.save(commit=False)
            project.author = request.user
            project.save()
            messages.success(request, f"Projeto '{project.title}' publicado com sucesso no seu portfólio!")
            return redirect('profile', username=request.user.username)
        else:
            messages.error(request, "Erro ao publicar o projeto. Verifique os campos.")
    
    return redirect('home')


@login_required(login_url='login')
def hire_creator_view(request, username):
    """
    Processa a solicitação de contratação/orçamento para um criador.
    """
    creator = get_object_or_404(User, username=username)

    if request.user == creator:
        messages.warning(request, "Não pode enviar uma proposta de contratação para o seu próprio perfil.")
        return redirect('profile', username=username)

    if request.method == 'POST':
        form = HiringRequestForm(request.POST)
        if form.is_valid():
            proposal = form.save(commit=False)
            proposal.creator = creator
            proposal.sender = request.user
            
            project_id = request.POST.get('project_id')
            if project_id:
                try:
                    proposal.project = Project.objects.get(id=project_id)
                except Project.DoesNotExist:
                    pass

            proposal.save()
            messages.success(request, f"Proposta enviada com sucesso para @{creator.username}! O criador entrará em contacto.")
        else:
            messages.error(request, "Erro ao enviar a proposta. Verifique os campos preenchidos.")

    # Redireciona de volta para onde o utilizador estava
    next_url = request.POST.get('next') or request.META.get('HTTP_REFERER')
    if next_url:
        return redirect(next_url)
    return redirect('profile', username=username)


@login_required(login_url='login')
def project_detail_view(request, project_id):
    """
    Exibe a página de detalhe da arte / projeto:
    - Visualização do vídeo ou arte com efeito CRT/scanlines
    - Opção de dar like e ver contagem
    - Opção de salvar a arte na lista pessoal
    - Opção de comprar o modelo 3D / asset da arte
    - Seção de comentários
    - Botão de excluir se for o autor
    - Proposta de parceria/colaboração com o criador
    """
    project = get_object_or_404(Project, id=project_id)
    
    # Incrementa contador de visualizações
    Project.objects.filter(id=project_id).update(views_count=project.views_count + 1)
    project.refresh_from_db()

    user_has_liked = request.user.is_authenticated and project.likes.filter(id=request.user.id).exists()
    user_has_saved = request.user.is_authenticated and project.saved_by.filter(id=request.user.id).exists()
    user_has_purchased = request.user.is_authenticated and ProjectPurchase.objects.filter(project=project, buyer=request.user).exists()
    is_owner = (request.user == project.author)

    comments = project.comments.all().select_related('author__profile')
    comment_form = ProjectCommentForm()
    hiring_form = HiringRequestForm()
    partnership_form = PartnershipProposalForm()

    context = {
        'project': project,
        'user_has_liked': user_has_liked,
        'user_has_saved': user_has_saved,
        'user_has_purchased': user_has_purchased,
        'is_owner': is_owner,
        'comments': comments,
        'comment_form': comment_form,
        'hiring_form': hiring_form,
        'partnership_form': partnership_form,
    }
    return render(request, 'project_detail.html', context)


@login_required(login_url='login')
def delete_project_view(request, project_id):
    """
    Permite ao autor do projeto remover sua publicação.
    """
    project = get_object_or_404(Project, id=project_id)

    if project.author != request.user:
        messages.error(request, "Você não tem permissão para remover este projeto.")
        return redirect('home')

    if request.method == 'POST':
        title = project.title
        project.delete()
        messages.success(request, f"O projeto '{title}' foi removido com sucesso!")
        return redirect('profile', username=request.user.username)

    # Se for GET, pede confirmação
    return render(request, 'project_confirm_delete.html', {'project': project})


@login_required(login_url='login')
def like_project_view(request, project_id):
    """
    Alterna a curtida (like/unlike) do utilizador no projeto.
    Suporta AJAX e redirecionamento comum.
    """
    project = get_object_or_404(Project, id=project_id)
    
    if project.likes.filter(id=request.user.id).exists():
        project.likes.remove(request.user)
        liked = False
    else:
        project.likes.add(request.user)
        liked = True

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'liked': liked,
            'total_likes': project.total_likes
        })

    next_url = request.POST.get('next') or request.META.get('HTTP_REFERER') or 'home'
    return redirect(next_url)


@login_required(login_url='login')
def save_project_view(request, project_id):
    """
    Alterna o salvamento (bookmark) do projeto na conta do utilizador.
    Suporta AJAX e redirecionamento comum.
    """
    project = get_object_or_404(Project, id=project_id)
    
    if project.saved_by.filter(id=request.user.id).exists():
        project.saved_by.remove(request.user)
        saved = False
        msg = f"Projeto '{project.title}' removido dos seus salvos."
    else:
        project.saved_by.add(request.user)
        saved = True
        msg = f"Projeto '{project.title}' salvo com sucesso no seu perfil!"

    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({
            'saved': saved,
            'total_saves': project.total_saves,
            'message': msg
        })

    messages.success(request, msg)
    next_url = request.POST.get('next') or request.META.get('HTTP_REFERER') or 'home'
    return redirect(next_url)


@login_required(login_url='login')
def propose_partnership_view(request, username):
    """
    Cria uma nova proposta de colaboração / parceria entre artistas.
    """
    receiver = get_object_or_404(User, username=username)

    if request.user == receiver:
        messages.warning(request, "Você não pode propor uma parceria a si mesmo.")
        return redirect('profile', username=username)

    if request.method == 'POST':
        form = PartnershipProposalForm(request.POST)
        if form.is_valid():
            proposal = form.save(commit=False)
            proposal.sender = request.user
            proposal.receiver = receiver

            project_id = request.POST.get('project_id')
            if project_id:
                try:
                    proposal.project = Project.objects.get(id=project_id)
                except Project.DoesNotExist:
                    pass

            proposal.save()

            if proposal.message:
                PartnershipMessage.objects.create(
                    partnership=proposal,
                    sender=request.user,
                    text=proposal.message
                )

            messages.success(request, f"Proposta de parceria enviada para @{receiver.username}! Vocês já podem conversar na aba de parcerias.")
            return redirect(f"/perfil/{request.user.username}/#parcerias")
        else:
            messages.error(request, "Erro ao enviar proposta de parceria. Verifique os campos preenchidos.")

    return redirect('profile', username=username)


@login_required(login_url='login')
def update_partnership_status_view(request, proposal_id, new_status):
    """
    Atualiza o status de uma parceria (aceita ou recusada).
    """
    proposal = get_object_or_404(PartnershipProposal, id=proposal_id)

    if request.user != proposal.receiver and request.user != proposal.sender:
        messages.error(request, "Você não tem permissão para alterar esta proposta.")
        return redirect(f"/perfil/{request.user.username}/#parcerias")

    if new_status in ['accepted', 'declined']:
        proposal.status = new_status
        proposal.save()
        if new_status == 'accepted':
            messages.success(request, f"Parceria com @{proposal.sender.username} aceita com sucesso! Vocês já podem co-criar projetos.")
        else:
            messages.info(request, "Proposta de parceria recusada.")

    return redirect(f"/perfil/{request.user.username}/#parcerias")


@login_required(login_url='login')
def send_partnership_message_view(request, proposal_id):
    """
    Envia uma mensagem direta dentro do chat de uma parceria específica.
    """
    proposal = get_object_or_404(PartnershipProposal, id=proposal_id)

    if request.user != proposal.sender and request.user != proposal.receiver:
        messages.error(request, "Você não participa desta conversa de parceria.")
        return redirect(f"/perfil/{request.user.username}/#parcerias")

    if request.method == 'POST':
        form = PartnershipMessageForm(request.POST)
        if form.is_valid():
            msg = form.save(commit=False)
            msg.partnership = proposal
            msg.sender = request.user
            msg.save()
            proposal.save()  # Atualiza timestamp updated_at
            messages.success(request, "Mensagem enviada com sucesso!")
        else:
            messages.error(request, "Não foi possível enviar a mensagem.")

    return redirect(f"/perfil/{request.user.username}/#parcerias")


@login_required(login_url='login')
def add_comment_view(request, project_id):
    """
    Adiciona um comentário à arte/projeto.
    """
    project = get_object_or_404(Project, id=project_id)

    if request.method == 'POST':
        form = ProjectCommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.project = project
            comment.author = request.user
            comment.save()
            messages.success(request, "Comentário publicado com sucesso!")
        else:
            messages.error(request, "Por favor, digite um comentário válido.")

    return redirect('project_detail', project_id=project.id)


@login_required(login_url='login')
def delete_comment_view(request, comment_id):
    """
    Permite ao dono da arte (project.author) ou ao próprio autor do comentário (comment.author)
    excluir um comentário.
    """
    comment = get_object_or_404(ProjectComment, id=comment_id)
    project_id = comment.project.id

    if request.user == comment.project.author or request.user == comment.author:
        comment.delete()
        messages.success(request, "Comentário excluído com sucesso!")
    else:
        messages.error(request, "Você não tem permissão para excluir este comentário.")

    return redirect('project_detail', project_id=project_id)


@login_required(login_url='login')
def update_project_price_view(request, project_id):
    """
    Permite ao autor do projeto escolher ou alterar o preço da arte diretamente na página de detalhes.
    """
    from decimal import Decimal, InvalidOperation
    project = get_object_or_404(Project, id=project_id)

    if project.author != request.user:
        messages.error(request, "Apenas o criador da arte pode alterar o preço base.")
        return redirect('project_detail', project_id=project.id)

    if request.method == 'POST':
        raw_price = request.POST.get('new_price', '').strip().replace(',', '.')
        try:
            new_price = Decimal(raw_price)
            if new_price < Decimal('0.00'):
                raise InvalidOperation
            project.price = new_price
            project.save(update_fields=['price'])
            messages.success(request, f"Preço da arte '{project.title}' atualizado para R$ {project.price:.2f}!")
        except (InvalidOperation, ValueError):
            messages.error(request, "Informe um valor numérico válido para o preço da arte.")

    return redirect('project_detail', project_id=project.id)


@login_required(login_url='login')
def buy_project_model_view(request, project_id):
    """
    Processa a compra do modelo 3D / Asset de Motion Design pelo preço fixo definido pelo dono da arte.
    """
    project = get_object_or_404(Project, id=project_id)

    if project.author == request.user:
        messages.info(request, "Você é o autor desta arte e já possui todos os arquivos originais.")
        return redirect('project_detail', project_id=project.id)

    if request.method == 'POST':
        purchase, created = ProjectPurchase.objects.get_or_create(
            project=project,
            buyer=request.user,
            defaults={'price_paid': project.price}
        )
        if created:
            messages.success(request, f"Parabéns! Você adquiriu '{project.title}' por R$ {project.price:.2f}! Chave de Licença: {purchase.license_key}")
        else:
            messages.info(request, f"Você já possui a licença deste projeto. Sua chave: {purchase.license_key}")

    return redirect('project_detail', project_id=project.id)


def logout_view(request):
    logout(request)
    messages.info(request, "Sessão terminada com sucesso. Até logo!")
    return redirect('landing')