from django import forms
from django.core.mail.message import EmailMessage
from .models import Register


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
        fields = ['name', 'status', 'photo']

