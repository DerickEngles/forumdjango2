from django.urls import path
from .views import index, message, register

urlpatterns = [
    path('', index, name='index'),
    path('contato/', message, name='message'),  # name é o apelido da url aqui no backend, diferentemente, dentro do
    # contato/ que é o que digito na barra de pesquisa para acessar tal página
    path('registro/', register, name='register'),
]
