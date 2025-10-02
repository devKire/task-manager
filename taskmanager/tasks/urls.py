from django.urls import path, include
from . import views

app_name = 'tasks'

urlpatterns = [
    path('', views.lista_tarefas, name='lista_tarefas'),
    path('concluir/<int:tarefa_id>/', views.marcar_concluida, name='marcar_concluida'),
    path('excluir/<int:tarefa_id>/', views.excluir_tarefa, name='excluir_tarefa'),
    path('editar/<int:tarefa_id>/', views.editar_tarefa, name='editar_tarefa'),
    
    # URLs para categorias
    path('categorias/', views.lista_categorias, name='lista_categorias'),
    path('categorias/excluir/<int:categoria_id>/', views.excluir_categoria, name='excluir_categoria'),
    
    # URLs de autenticação
    path('registrar/', views.registrar, name='registrar'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),  # Atualizada para nossa view personalizada
    path('', include('pwa.urls')),
]