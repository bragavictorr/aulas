from django.urls import path
from core import views

urlpatterns = [
    path('', views.landing_page, name='landing'),
    path('login/', views.login_view, name='login'),
    path('cadastro/', views.cadastro_view, name='cadastro'),
    path('feed/', views.home_feed, name='home'),
    path('logout/', views.logout_view, name='logout'),
    path('perfil/<str:username>/', views.profile_view, name='profile'),
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
]