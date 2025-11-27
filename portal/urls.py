from django.urls import path
from . import views

app_name = 'portal'

urlpatterns = [
    path('', views.home, name='home'),
    path('tema/<slug:tema_slug>/', views.editoriais_por_tema, name='tema'),
    path('editorial/<int:pk>/', views.detalhe_editorial, name='detalhe'),
    path('buscar/', views.buscar, name='buscar'),
    path('autores/', views.listar_autores, name='autores'),
    path('autor/<str:apelido>/', views.detalhe_autor, name='detalhe_autor'),
    path('api/inscrever-newsletter/', views.inscrever_newsletter, name='inscrever_newsletter'),
    path('api/cancelar-newsletter/', views.cancelar_newsletter, name='cancelar_newsletter'),
    path('api/temas/', views.listar_temas_api, name='listar_temas'),
]
