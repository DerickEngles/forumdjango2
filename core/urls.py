from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import index, message, register, post, creatpost, userdatachange, recoverdata, deletepost, updatepost

urlpatterns = [
    path('', index, name='index'),
    path('contato/', message, name='message'),  # name é o apelido da url aqui no backend, diferentemente, dentro do
    # contato/ que é o que digito na barra de pesquisa para acessar tal página
    path('registro/', register, name='register'),
    path('postagens/', post, name='posts'),
    path('criarpostagem/', creatpost, name='creatpost'),
    # views do próprio Django para autenticação (login e logout)
    path('login/', LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', LogoutView.as_view(next_page='index'), name='logout'),
    path('alterardados/', userdatachange, name='userdatachange'),
    path('recuperardados/', recoverdata, name='recoverdata'),
    path('deletarpost/<int:post_id>/', deletepost, name='deletepost'),
    path('atualizarpost/<int:post_id>/', updatepost, name='updatepost')  # devo passar post_id como referência ao
    # post.id não posso passar post.id, pois a url não pode ter acesso direto a esse valor.
]
"""
para resumir:

message é uma referência à função message. O Django chama essa função apenas quando a rota correspondente é acessada.
message() é a invocação imediata da função message. Isso executa a função no momento em que o arquivo de URLs é lido ou 
importado, não quando a rota é acessada.

Não queremos as funções/views sejam executadas até que exista uma interação por parte do usuário com elas.
"""
