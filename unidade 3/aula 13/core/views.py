from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.db import transaction
from django.db.models import Q, Count
from django.http import JsonResponse
from django.utils import timezone
from datetime import timedelta
from decimal import Decimal, InvalidOperation
import os
import re
import uuid
import requests
from django.conf import settings
from django.http import HttpResponseRedirect, HttpResponse


from .forms import (
    CustomUserCreationForm, UserProfileForm, UserUpdateForm,
    HiringRequestForm, ProjectForm, ProjectCommentForm,
    PartnershipProposalForm, PartnershipMessageForm, UserSuggestionForm
)
from .models import (
    UserProfile, Project, HiringRequest, ProjectComment, ProjectPurchase,
    PartnershipProposal, PartnershipMessage, UserSuggestion, UserFollow, Notification
)


def landing_page(request):
    # Anotação de curtidas reais em cada projeto
    annotated_projects = Project.objects.all().select_related('author__profile').annotate(
        num_likes=Count('likes')
    )

    # 1. Arte Mais Curtida da Semana (últimos 7 dias)
    one_week_ago = timezone.now() - timedelta(days=7)
    weekly_projects = annotated_projects.filter(created_at__gte=one_week_ago).order_by('-num_likes', '-created_at')

    motion_of_the_day = weekly_projects.first() if weekly_projects.exists() else None

    # Fallback: se não houver projetos recentes na semana ou se o top da semana tiver 0 curtidas
    # enquanto houver outros projetos da comunidade com curtidas, destaca o mais curtido geral
    if not motion_of_the_day or (motion_of_the_day.num_likes == 0 and annotated_projects.filter(num_likes__gt=0).exists()):
        motion_of_the_day = annotated_projects.order_by('-num_likes', '-created_at').first()

    featured_projects = annotated_projects.order_by('-num_likes', '-created_at')[:6]
    
    total_projects = Project.objects.count()
    total_creators = User.objects.count()
    
    # Calcular contagem estimada de visualizações e curtidas totais
    views_sum = sum(Project.objects.values_list('views_count', flat=True)) or 0
    likes_sum = sum(p.total_likes for p in Project.objects.all()) or 0
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
            # Limpa mensagens residuais pendentes de sessões anteriores
            storage = messages.get_messages(request)
            for _ in storage:
                pass
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
            # Limpa mensagens residuais pendentes (ex: logout da sessão anterior)
            storage = messages.get_messages(request)
            for _ in storage:
                pass
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

    initial_query = request.GET.get('q', '').strip()

    # Publicações de criadores que o usuário segue
    following_ids = list(UserFollow.objects.filter(follower=request.user).values_list('following_id', flat=True))
    following_projects = Project.objects.filter(author_id__in=following_ids).select_related('author__profile')

    # Sugestões de criadores para seguir
    suggested_creators = User.objects.exclude(id=request.user.id).exclude(id__in=following_ids).select_related('profile').filter(projects__isnull=False).distinct()[:5]

    return render(request, 'home.html', {
        'projects': projects,
        'following_projects': following_projects,
        'following_count': len(following_ids),
        'suggested_creators': suggested_creators,
        'total_projects': total_projects,
        'total_users': total_users,
        'total_creators': total_creators,
        'hiring_form': hiring_form,
        'project_form': project_form,
        'initial_query': initial_query,
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
    partnerships_accepted = []
    partnerships_pending = []
    partnership_message_form = None

    has_edit_errors = False

    if is_own_profile:
        received_proposals = HiringRequest.objects.filter(creator=target_user)
        saved_projects = target_user.saved_projects.all().select_related('author__profile')
        liked_projects = target_user.liked_projects.all().select_related('author__profile')
        partnerships = PartnershipProposal.objects.filter(
            Q(sender=target_user) | Q(receiver=target_user)
        ).select_related('sender__profile', 'receiver__profile', 'project').prefetch_related('messages__sender__profile').distinct()
        partnerships_accepted = partnerships.filter(status='accepted')
        partnerships_pending = partnerships.filter(status='pending')
        partnership_message_form = PartnershipMessageForm()
        
        if request.method == 'POST':
            # Atualização do perfil e foto de avatar
            user_form = UserUpdateForm(request.POST, instance=target_user)
            profile_form = UserProfileForm(request.POST, request.FILES, instance=profile)

            if user_form.is_valid() and profile_form.is_valid():
                with transaction.atomic():
                    user_form.save()
                    profile_form.save()
                messages.success(request, "Seu perfil e imagens foram atualizados com sucesso!")
                return redirect('profile', username=target_user.username)
            else:
                has_edit_errors = True
                messages.error(request, "Por favor, corrija os erros no formulário.")
        else:
            user_form = UserUpdateForm(instance=target_user)
            profile_form = UserProfileForm(instance=profile)

    hiring_form = HiringRequestForm()
    partnership_form = PartnershipProposalForm()
    project_form = ProjectForm()

    followers_count = target_user.followers_relations.count()
    following_count = target_user.following_relations.count()
    is_following = (
        request.user.is_authenticated 
        and not is_own_profile 
        and UserFollow.objects.filter(follower=request.user, following=target_user).exists()
    )

    followers_list = (
        UserFollow.objects.filter(following=target_user)
        .select_related('follower__profile')
        .annotate(projects_count=Count('follower__projects', distinct=True))
    )
    following_list = (
        UserFollow.objects.filter(follower=target_user)
        .select_related('following__profile')
        .annotate(projects_count=Count('following__projects', distinct=True))
    )
    current_user_following_ids = set(
        UserFollow.objects.filter(follower=request.user).values_list('following_id', flat=True)
    ) if request.user.is_authenticated else set()

    context = {
        'target_user': target_user,
        'profile': profile,
        'is_own_profile': is_own_profile,
        'has_edit_errors': has_edit_errors,
        'followers_count': followers_count,
        'following_count': following_count,
        'is_following': is_following,
        'followers_list': followers_list,
        'following_list': following_list,
        'current_user_following_ids': current_user_following_ids,
        'projects': projects,
        'saved_projects': saved_projects,
        'liked_projects': liked_projects,
        'partnerships': partnerships,
        'partnerships_accepted': partnerships_accepted,
        'partnerships_pending': partnerships_pending,
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
def update_cover_image_view(request):
    """
    Atualiza a imagem de capa panorâmica do usuário logado via AJAX ou formulário direto.
    """
    if request.method == 'POST':
        cover_file = request.FILES.get('cover_image')
        if not cover_file:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'error': 'Nenhuma imagem foi selecionada.'}, status=400)
            messages.error(request, "Nenhuma imagem foi selecionada para a capa.")
            return redirect('profile', username=request.user.username)

        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        profile.cover_image = cover_file
        profile.save(update_fields=['cover_image'])

        msg = "Foto de capa atualizada com sucesso!"
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'status': 'ok',
                'cover_url': profile.cover_image.url,
                'message': msg
            })
        messages.success(request, msg)

    return redirect('profile', username=request.user.username)


@login_required(login_url='login')
def update_avatar_view(request):
    """
    Atualiza a foto de avatar do usuário logado via AJAX ou formulário direto.
    """
    if request.method == 'POST':
        avatar_file = request.FILES.get('avatar')
        if not avatar_file:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'error': 'Nenhuma foto foi selecionada.'}, status=400)
            messages.error(request, "Nenhuma foto foi selecionada para o avatar.")
            return redirect('profile', username=request.user.username)

        profile, _ = UserProfile.objects.get_or_create(user=request.user)
        profile.avatar = avatar_file
        profile.save(update_fields=['avatar'])

        msg = "Foto de perfil atualizada com sucesso!"
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'status': 'ok',
                'avatar_url': profile.avatar.url,
                'message': msg
            })
        messages.success(request, msg)

    return redirect('profile', username=request.user.username)


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
            error_details = []
            for field, errors in form.errors.items():
                label = form.fields[field].label if field in form.fields else field
                error_details.append(f"{label}: {', '.join(errors)}")
            messages.error(request, f"Erro ao publicar o projeto: {' | '.join(error_details)}")
    
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

            # Garantir formatação em Real (R$) para o orçamento
            if proposal.budget:
                b_str = proposal.budget.strip()
                if not b_str.startswith('R$'):
                    raw_digits = re.sub(r'\D', '', b_str)
                    if raw_digits:
                        try:
                            num = float(raw_digits)
                            if ',' in b_str:
                                num = num / 100
                            proposal.budget = f"R$ {num:,.2f}".replace(',', 'X').replace('.', ',').replace('X', '.')
                        except Exception:
                            proposal.budget = f"R$ {b_str}"
                    else:
                        proposal.budget = f"R$ {b_str}"

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

    is_following_author = (
        request.user.is_authenticated 
        and not is_owner 
        and UserFollow.objects.filter(follower=request.user, following=project.author).exists()
    )
    author_followers_count = project.author.followers_relations.count()

    context = {
        'project': project,
        'user_has_liked': user_has_liked,
        'user_has_saved': user_has_saved,
        'user_has_purchased': user_has_purchased,
        'is_owner': is_owner,
        'is_following_author': is_following_author,
        'author_followers_count': author_followers_count,
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

    # Manter likes_count sincronizado no banco de dados
    project.likes_count = project.likes.count()
    project.save(update_fields=['likes_count'])

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
            return redirect(f"/perfil/{request.user.username}/#parcerias-aceitas")
        else:
            messages.info(request, "Proposta de parceria recusada.")
            return redirect(f"/perfil/{request.user.username}/#parcerias-pendentes")

    return redirect(f"/perfil/{request.user.username}/#parcerias-aceitas")


@login_required(login_url='login')
def send_partnership_message_view(request, proposal_id):
    """
    Envia uma mensagem direta dentro do chat de uma parceria específica.
    Suporta envio assíncrono (AJAX) para uma troca de mensagens super fluida sem recarregar a tela.
    """
    proposal = get_object_or_404(PartnershipProposal, id=proposal_id)

    if request.user != proposal.sender and request.user != proposal.receiver:
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': False, 'message': 'Você não participa desta conversa de parceria.'}, status=403)
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

            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'message': {
                        'id': msg.id,
                        'text': msg.text,
                        'created_at': msg.created_at.strftime('%d/%m %H:%M'),
                        'sender_username': msg.sender.username,
                        'is_mine': True,
                    }
                })

            messages.success(request, "Mensagem enviada com sucesso!")
        else:
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'message': 'Não foi possível enviar a mensagem.'}, status=400)
            messages.error(request, "Não foi possível enviar a mensagem.")

    return redirect(f"/perfil/{request.user.username}/#parcerias")


@login_required(login_url='login')
def get_partnership_messages_view(request, proposal_id):
    """
    Retorna as mensagens em tempo real de uma parceria específica via JSON para polling fluido.
    """
    proposal = get_object_or_404(PartnershipProposal, id=proposal_id)
    if request.user != proposal.sender and request.user != proposal.receiver:
        return JsonResponse({'success': False, 'message': 'Não autorizado.'}, status=403)

    messages_list = []
    for msg in proposal.messages.all():
        messages_list.append({
            'id': msg.id,
            'text': msg.text,
            'created_at': msg.created_at.strftime('%d/%m %H:%M'),
            'sender_username': msg.sender.username,
            'is_mine': (msg.sender == request.user),
        })

    return JsonResponse({'success': True, 'messages': messages_list})


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
    Permite ao autor do projeto escolher ou alterar o preço da arte diretamente na página de detalhes,
    ou ativar/desativar a venda da arte (definindo apenas para exibição/portfólio).
    """
    project = get_object_or_404(Project, id=project_id)
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest' or 'application/json' in request.headers.get('Accept', '')

    if project.author != request.user:
        if is_ajax:
            return JsonResponse({'success': False, 'error': "Apenas o criador da arte pode alterar o preço base e opções de venda."}, status=403)
        messages.error(request, "Apenas o criador da arte pode alterar o preço base e opções de venda.")
        return redirect('project_detail', project_id=project.id)

    if request.method == 'POST':
        is_for_sale_val = request.POST.get('is_for_sale')
        is_for_sale = is_for_sale_val in ['1', 'true', 'on', True]
        raw_price = request.POST.get('new_price', '').strip().replace(',', '.')

        if not is_for_sale:
            project.is_for_sale = False
            project.price = Decimal('0.00')
            project.save(update_fields=['is_for_sale', 'price'])
            msg = f"Venda desativada! A arte '{project.title}' foi definida como obra de portfólio. Outras pessoas não poderão comprar nem baixar os arquivos."
            if is_ajax:
                return JsonResponse({
                    'success': True,
                    'is_for_sale': False,
                    'price': '0.00',
                    'formatted_price': '0,00',
                    'message': msg
                })
            messages.success(request, msg)
        else:
            try:
                new_price = Decimal(raw_price) if raw_price else Decimal('29.90')
                if new_price < Decimal('0.00'):
                    raise InvalidOperation
                project.price = new_price
                project.is_for_sale = True
                project.save(update_fields=['is_for_sale', 'price'])
                msg = f"Sucesso! A arte '{project.title}' está à venda por R$ {project.price:.2f}. Os outros usuários agora podem comprar e baixar os arquivos."
                if is_ajax:
                    return JsonResponse({
                        'success': True,
                        'is_for_sale': True,
                        'price': f"{project.price:.2f}",
                        'formatted_price': f"{project.price:.2f}".replace('.', ','),
                        'message': msg
                    })
                messages.success(request, msg)
            except (InvalidOperation, ValueError):
                err_msg = "Informe um valor numérico válido para o preço da arte."
                if is_ajax:
                    return JsonResponse({'success': False, 'error': err_msg}, status=400)
                messages.error(request, err_msg)

    return redirect('project_detail', project_id=project.id)


@login_required(login_url='login')
def buy_project_model_view(request, project_id):
    """
    Processa a compra do modelo 3D / Asset de Motion Design pelo preço fixo definido pelo dono da arte.
    Se a arte não estiver à venda, impede a compra ou download.
    """
    project = get_object_or_404(Project, id=project_id)

    if project.author == request.user:
        messages.info(request, "Você é o autor desta arte e já possui todos os arquivos originais.")
        return redirect('project_detail', project_id=project.id)

    if not project.is_for_sale:
        messages.error(request, "Esta arte não está à venda. Seus arquivos foram disponibilizados pelo autor apenas para visualização e portfólio, não sendo possível comprar ou baixar.")
        return redirect('project_detail', project_id=project.id)

    if request.method == 'POST':
        price_to_pay = project.price if project.price and project.price > 0 else Decimal('0.00')
        purchase, created = ProjectPurchase.objects.get_or_create(
            project=project,
            buyer=request.user,
            defaults={'price_paid': price_to_pay}
        )
        if created:
            messages.success(request, f"Parabéns! Você adquiriu '{project.title}' por R$ {purchase.price_paid:.2f}! Chave de Licença: {purchase.license_key}")
        else:
            messages.info(request, f"Você já possui a licença deste projeto. Sua chave: {purchase.license_key}")

    return redirect('project_detail', project_id=project.id)


def logout_view(request):
    logout(request)
    messages.info(request, "Sessão terminada com sucesso. Até logo!")
    return redirect('landing')
def criar_pagamento(request):
    """
    Cria uma ordem de pagamento no Mercado Pago e redireciona o usuário para o Checkout.
    Suporta compra de projetos específicos via GET/POST 'project_id' ou teste padrão.
    """
    access_token = getattr(settings, 'MP_ACCESS_TOKEN', None) or os.environ.get("MP_ACCESS_TOKEN")
    
    if not access_token:
        return HttpResponse(
            "<h3>Erro de Configuração</h3>"
            "<p>A variável <code>MP_ACCESS_TOKEN</code> não está configurada no seu arquivo <code>.env</code>.</p>",
            status=500
        )

    # Chave de idempotência para evitar pedidos duplicados
    idem_key = str(uuid.uuid4())

    # Dados do pedido (projeto específico ou teste padrão)
    project_id = request.GET.get('project_id') or request.POST.get('project_id')
    item_title = "Produto Vendas de Motion"
    item_price = "50.00"
    ext_ref = f"pedido_motion_{uuid.uuid4().hex[:6]}"
    payer_email = "comprador_teste@email.com"

    if request.user.is_authenticated and request.user.email:
        payer_email = request.user.email

    if project_id:
        try:
            proj = Project.objects.get(id=project_id)
            item_title = f"ArtFlow: {proj.title}"[:120]
            item_price = f"{proj.price:.2f}"
            ext_ref = f"artflow_proj_{proj.id}_{uuid.uuid4().hex[:6]}"
        except Project.DoesNotExist:
            pass

    # Payload formatado conforme a API v1/orders do Mercado Pago
    payload = {
        "type": "online",
        "processing_mode": "manual",
        "total_amount": item_price,
        "external_reference": ext_ref,
        "payer": {"email": payer_email},
        "items": [
            {
                "title": item_title,
                "quantity": 1,
                "unit_price": item_price
            }
        ]
    }

    try:
        # Faz a requisição para a API de Orders do Mercado Pago
        resp = requests.post(
            "https://api.mercadopago.com/v1/orders",
            json=payload,
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json",
                "X-Idempotency-Key": idem_key,
            },
            timeout=20,
        )

        if resp.status_code in (200, 201):
            checkout_url = resp.json().get("checkout_url")
            if checkout_url:
                return HttpResponseRedirect(checkout_url)
            return HttpResponse(
                f"Erro Mercado Pago: link de checkout não encontrado. Resposta: {resp.text}",
                status=500
            )
        else:
            return HttpResponse(
                f"<h3>Erro na API do Mercado Pago ({resp.status_code})</h3>"
                f"<p>Verifique as credenciais ou dados do pedido.</p>"
                f"<pre>{resp.text}</pre>",
                status=resp.status_code
            )
    except requests.exceptions.RequestException as exc:
        return HttpResponse(
            f"<h3>Erro de Conexão com Mercado Pago</h3><p>{exc}</p>",
            status=502
        )


def search_api_view(request):
    """
    Endpoint para busca em tempo real de usuários cadastrados e projetos.
    Permite encontrar qualquer pessoa que fez cadastro no site,
    mesmo que ainda não tenha publicado projetos.
    """
    query = request.GET.get('q', '').strip()

    if not query:
        return JsonResponse({'users': [], 'projects': []})

    # Busca em usuários cadastrados (username, primeiro nome, último nome, especialidade e biografia)
    users_qs = User.objects.filter(
        Q(username__icontains=query) |
        Q(first_name__icontains=query) |
        Q(last_name__icontains=query) |
        Q(profile__especialidade__icontains=query) |
        Q(profile__bio__icontains=query)
    ).select_related('profile').distinct()[:8]

    users_list = []
    for u in users_qs:
        avatar_url = None
        especialidade = ""
        if hasattr(u, 'profile'):
            if u.profile.avatar:
                avatar_url = u.profile.avatar.url
            especialidade = u.profile.especialidade or "Criador ArtFlow"

        display_name = u.get_full_name() or u.username
        users_list.append({
            'username': u.username,
            'name': display_name,
            'avatar_url': avatar_url,
            'initials': u.username[:1].upper(),
            'especialidade': especialidade,
            'projects_count': u.projects.count(),
            'profile_url': f"/perfil/{u.username}/",
        })

    return JsonResponse({
        'users': users_list,
        'projects': [],
    })


def submit_suggestion_view(request):
    """
    Recebe sugestões, ideias de novas ferramentas ou relatos de melhorias enviados pelos usuários.
    Suporta envio assíncrono via AJAX e formulário padrão.
    """
    if request.method == 'POST':
        form = UserSuggestionForm(request.POST)
        if form.is_valid():
            suggestion = form.save(commit=False)
            if request.user.is_authenticated:
                suggestion.user = request.user
                if not suggestion.name:
                    suggestion.name = request.user.get_full_name() or request.user.username
                if not suggestion.email and request.user.email:
                    suggestion.email = request.user.email
            suggestion.save()

            msg = "Muito obrigado pela sua sugestão! A sua ideia foi enviada com sucesso para nossa equipe."
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': True, 'message': msg})

            messages.success(request, msg)
        else:
            msg = "Erro ao enviar sugestão. Por favor, preencha todos os campos obrigatórios."
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({'success': False, 'message': msg}, status=400)

            messages.error(request, msg)

    next_url = request.POST.get('next') or request.META.get('HTTP_REFERER') or '/'
    return redirect(next_url)


@login_required(login_url='login')
def toggle_follow_view(request, username):
    """
    Permite a um usuário logado seguir ou deixar de seguir outro artista.
    Suporta requisições assíncronas (AJAX / fetch) e redirecionamento padrão.
    """
    target_user = get_object_or_404(User, username=username)
    is_ajax = request.headers.get('x-requested-with') == 'XMLHttpRequest' or 'application/json' in request.headers.get('Accept', '')

    if request.user == target_user:
        if is_ajax:
            return JsonResponse({'success': False, 'error': 'Você não pode seguir seu próprio perfil.'}, status=400)
        messages.warning(request, "Você não pode seguir seu próprio perfil.")
        return redirect('profile', username=username)

    follow_rel = UserFollow.objects.filter(follower=request.user, following=target_user)
    if follow_rel.exists():
        follow_rel.delete()
        is_following = False
        msg = f"Você deixou de seguir @{target_user.username}."
    else:
        UserFollow.objects.create(follower=request.user, following=target_user)
        is_following = True
        msg = f"Você agora está seguindo @{target_user.username}!"

        # Envia notificação em tempo real para o usuário que foi seguido
        Notification.objects.create(
            recipient=target_user,
            sender=request.user,
            notification_type='follow',
            title=f"@{request.user.username} começou a te seguir",
            message=f"@{request.user.username} começou a te seguir no ArtFlow e agora acompanha seus projetos.",
            link=f"/perfil/{request.user.username}/"
        )

    followers_count = target_user.followers_relations.count()
    following_count = target_user.following_relations.count()

    if is_ajax:
        return JsonResponse({
            'success': True,
            'status': 'ok',
            'is_following': is_following,
            'followers_count': followers_count,
            'following_count': following_count,
            'message': msg
        })

    messages.success(request, msg)
    next_url = request.POST.get('next') or request.META.get('HTTP_REFERER') or f'/perfil/{username}/'
    return redirect(next_url)


@login_required(login_url='login')
def mark_notifications_read_view(request):
    """
    Marca as notificações do usuário como lidas via AJAX ou redirecionamento.
    """
    if request.method == 'POST':
        Notification.objects.filter(recipient=request.user, is_read=False).update(is_read=True)
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'status': 'ok'})
    return redirect(request.META.get('HTTP_REFERER', 'home'))


@login_required(login_url='login')
def mark_single_notification_read_view(request, notif_id):
    """
    Marca uma notificação individual como lida e redireciona para o link de destino.
    """
    notif = get_object_or_404(Notification, id=notif_id, recipient=request.user)
    notif.is_read = True
    notif.save()
    if request.headers.get('x-requested-with') == 'XMLHttpRequest':
        return JsonResponse({'success': True, 'status': 'ok'})
    return redirect(notif.link or 'home')


@login_required(login_url='login')
def delete_single_notification_view(request, notif_id):
    """
    Exclui uma notificação específica do usuário.
    """
    notif = get_object_or_404(Notification, id=notif_id, recipient=request.user)
    notif.delete()
    if request.headers.get('x-requested-with') == 'XMLHttpRequest' or request.method == 'POST':
        unread_count = Notification.objects.filter(recipient=request.user, is_read=False).count()
        total_count = Notification.objects.filter(recipient=request.user).count()
        return JsonResponse({'success': True, 'status': 'ok', 'unread_count': unread_count, 'total_count': total_count})
    return redirect(request.META.get('HTTP_REFERER', 'home'))


@login_required(login_url='login')
def clear_all_notifications_view(request):
    """
    Exclui todas as notificações do usuário logado para deixar a caixa 100% limpa.
    """
    if request.method == 'POST' or request.headers.get('x-requested-with') == 'XMLHttpRequest':
        Notification.objects.filter(recipient=request.user).delete()
        if request.headers.get('x-requested-with') == 'XMLHttpRequest':
            return JsonResponse({'success': True, 'status': 'ok'})
    return redirect(request.META.get('HTTP_REFERER', 'home'))


@login_required(login_url='login')
def get_unread_notifications_api(request):
    """
    Retorna as notificações não lidas e recentes em tempo real via JSON.
    Permite polling contínuo para exibir alerta Toast na tela e atualizar contador.
    """
    unread_qs = Notification.objects.filter(recipient=request.user, is_read=False).order_by('-created_at')
    unread_count = unread_qs.count()
    
    recent_qs = Notification.objects.filter(recipient=request.user).order_by('-created_at')[:15]
    
    notifs_list = []
    for n in recent_qs:
        avatar_url = None
        if n.sender and hasattr(n.sender, 'profile') and n.sender.profile.avatar:
            avatar_url = n.sender.profile.avatar.url
        sender_initial = n.sender.username[:1].upper() if n.sender else "?"

        notifs_list.append({
            'id': n.id,
            'title': n.title,
            'message': n.message,
            'link': n.link or (f"/perfil/{n.sender.username}/" if n.sender else "#"),
            'is_read': n.is_read,
            'sender_username': n.sender.username if n.sender else "Sistema",
            'sender_avatar': avatar_url,
            'sender_initial': sender_initial,
            'created_at': n.created_at.strftime("%d/%m %H:%M"),
        })

    return JsonResponse({
        'status': 'ok',
        'unread_count': unread_count,
        'notifications': notifs_list
    })