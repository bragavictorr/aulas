from django.urls import path
from core import views


urlpatterns = [
    path('', views.landing_page, name='landing'),
    path('login/', views.login_view, name='login'),
    path('cadastro/', views.cadastro_view, name='cadastro'),
    path('feed/', views.home_feed, name='home'),
    path('logout/', views.logout_view, name='logout'),
    path('perfil/<str:username>/', views.profile_view, name='profile'),
    path('perfil/<str:username>/seguir/', views.toggle_follow_view, name='toggle_follow'),
    path('perfil/foto/atualizar-capa/', views.update_cover_image_view, name='update_cover_image'),
    path('perfil/foto/atualizar-avatar/', views.update_avatar_view, name='update_avatar'),
    path('adicionar-projeto/', views.add_project_view, name='add_project'),
    path('contratar/<str:username>/', views.hire_creator_view, name='hire_creator'),
    
    # Rotas de detalhe da arte, curtida, exclusão, comentários e compra do modelo
    path('projeto/<int:project_id>/', views.project_detail_view, name='project_detail'),
    path('projeto/<int:project_id>/excluir/', views.delete_project_view, name='delete_project'),
    path('projeto/<int:project_id>/curtir/', views.like_project_view, name='like_project'),
    path('projeto/<int:project_id>/salvar/', views.save_project_view, name='save_project'),
    path('projeto/<int:project_id>/comentar/', views.add_comment_view, name='add_comment'),
    path('comentario/<int:comment_id>/excluir/', views.delete_comment_view, name='delete_comment'),
    path('projeto/<int:project_id>/comprar/', views.buy_project_model_view, name='buy_project_model'),
    path('projeto/<int:project_id>/preco/', views.update_project_price_view, name='update_project_price'),

    # Rotas de Parcerias e Colaborações entre Artistas
    path('parceria/<str:username>/propor/', views.propose_partnership_view, name='propose_partnership'),
    path('parceria/<int:proposal_id>/status/<str:new_status>/', views.update_partnership_status_view, name='update_partnership_status'),
    path('parceria/<int:proposal_id>/mensagem/', views.send_partnership_message_view, name='send_partnership_message'),
    path('parceria/<int:proposal_id>/mensagens/', views.get_partnership_messages_view, name='get_partnership_messages'),
    path('comprar-teste/', views.criar_pagamento, name='criar_pagamento'),
    path('api/buscar/', views.search_api_view, name='search_api'),
    path('sugestoes/enviar/', views.submit_suggestion_view, name='submit_suggestion'),
    path('notificacoes/marcar-lidas/', views.mark_notifications_read_view, name='mark_notifications_read'),
    path('notificacoes/limpar-tudo/', views.clear_all_notifications_view, name='clear_all_notifications'),
    path('notificacoes/<int:notif_id>/ler/', views.mark_single_notification_read_view, name='mark_single_notification_read'),
    path('notificacoes/<int:notif_id>/excluir/', views.delete_single_notification_view, name='delete_single_notification'),
    path('api/notificacoes/recentes/', views.get_unread_notifications_api, name='api_unread_notifications'),
]


