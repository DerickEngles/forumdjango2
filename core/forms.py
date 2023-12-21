from django import forms
from django.core.mail.message import EmailMessage
from .models import Register, Post
from django.contrib.auth.models import User
# from django.contrib.auth.forms import UserCreationForm
"""
UserCreationForm é uma classe fornecida pelo Django que é utilizada para criar formulários de criação de usuário. É 
especialmente útil quando você está lidando com a criação de novos usuários em um sistema Django. Este formulário cuida 
dos campos comuns necessários para criar um novo usuário, como nome de usuário, senha e confirmação de senha.

Ao usar UserCreationForm, o Django lida automaticamente com a validação dos campos, incluindo a verificação se as senhas
coincidem e se o nome de usuário é único. Ele também possui métodos e funcionalidades úteis, tornando mais simples a 
criação de formulários de registro de usuário personalizados.
"""


class MessageForm(forms.Form):
    # Vamos colocar os campos que o meu forms de mensagem terá
    name = forms.CharField(label='Nome', max_length=100)  # Vou fazer referência a name na minha view
    email = forms.EmailField(label='E-mail', max_length=100)
    subject = forms.CharField(label='Assunto', max_length=120)
    message = forms.CharField(label='Mensagem', widget=forms.Textarea())

    def send_email(self):  # Função que criamos para disparar e-mail.
        name = self.cleaned_data['name']
        email = self.cleaned_data['email']
        subject = self.cleaned_data['subject']
        message = self.cleaned_data['message']

        content = f'Nome: {name}\nE-mail: {email}\n Assunto: {subject}\n Mensagem: {message}'

        mail = EmailMessage(
            subject='Email enviado pelo sistema ForumDjango',
            body=content,
            from_email='contato@forumdjango.com.br',
            to=['contato@forumdjango.com.br', 'adminforumdjango@gmail.com'],
            headers={f'Reply-to': email}
        )
        mail.send()


class RegisterModelForm(forms.ModelForm):

    class Meta:
        model = Register
        fields = ['username', 'email', 'password', 'status', 'photo']

"""
Estamos utilizando um form que a view de autenticação do Django já possui. Portanto podemos descartar esse formulário.

class LoginForm(forms.Form):
    email = forms.EmailField(label='E-mail', max_length=100)
    password = forms.CharField(label='Senha', max_length=100)
"""


class PostModelForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = ['title', 'subject', 'text', 'photo']


class UserDataChangeModelForm(forms.ModelForm):

    class Meta:
        model = Register  # Ele vai herdar de Register, pois os campos a serem preenchidos serão os mesmos
        fields = ['username', 'email', 'password', 'status', 'photo']


class RecoverDatasForm(forms.Form):

    email = forms.EmailField(label='E-mail', max_length=100)

    def send_email(self):
        email = self.cleaned_data['email']
        user_django = User.objects.filter(email=email).first()
        user_database = Register.objects.filter(email=email).first()

        content = f'No DjangoDatabase:\nNome: {user_django.username}\nSenha: {user_django.password}\n' \
                  f'No MySQL: \n Nome: {user_database.username}\nSenha: {user_database.password}'
        # A senha é criptografada, pois ela está vindo do usuário Django, diferente da senha que está registrada no
        # banco de dados MySQL

        mail = EmailMessage(
            subject='Email enviado pelo sistema Fórum Django',
            body=content,
            from_email='contato@forumdjango.com.br',
            to=[f'contato@forumdjango.com.br', 'adminforumdjango@gmail.com', {user_django.email}],
        )
        mail.send()


class UpdatePostModelForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'subject', 'text', 'photo']
        # Isso aqui representa a ordem de exibição dos atributos na página
