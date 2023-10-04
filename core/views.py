from django.shortcuts import render
from django.contrib import messages  # Esse messages está vindo do meu contato.html

from .forms import MessageForm, RegisterModelForm

from . models import Register  # O model Register vai trazer os dados diretamente do banco de dados para minha via index


def index(request):
    context = {
        'registers': Register.objects.all()
    }
    return render(request, 'index.html', context)


def message(request):
    message_form = MessageForm(request.POST or None)  # O formulário pode ter dados ou estar vazio (usualmente, quando
    # o usuário abrir a página apenas, teremos um form do tipo None.
    if str(request.method) == 'POST':
        if message_form.is_valid():  # Função da classe Form
            message_form.send_email()  # função que criamos na nossa classe forms
    # Vou precisar checar se o método é do tipo POST ou
            message_form = MessageForm() # Estamos passando o formulário vazio
            messages.success(request, 'Mensagem enviada com sucesso!')
        else:
            messages.error(request, 'Erro ao enviar mensagem!')

    context = {  # Garante que seja passado para o HTML um forms com aparência/campos que foram criados em forms
        'message_form': message_form
    }
    return render(request, 'contact.html', context)

# Fazer uma modificação em register, pois quero que os usuário sejam redirecionados para index após o registro bem
# sucedido. Será que é só inserir o return com index dentro do if????
def register(request):
    # print(request.user)  # para saber o tipo de usuário que acessa a página registro. Um AnonymousUser consegue aces
    # sar. No caso desse nosso progrma deve ser desse jeito, pois quero cadastrar diferentes usuários.
    if str(request.method) == 'POST':
        form = RegisterModelForm(request.POST, request.FILES)  # variável que vai salvar os dados que vierem request
        # POST (inseridos no Template) e request.Files será um diretório com imagens
        if form.is_valid(): # is_valid é uma das funções de form
            form.save()  # para salvar no banco de dados
            messages.success(request, 'Usuário cadastrado com sucesso!')
            form = RegisterModelForm()  # Garantindo que o template receba um novo form limpo para o cadastrado de novo
            # usuário para ser passado para o contexto
        else:
            messages.error(request, 'Erro ao cadastrar usuário!')
    else:  # Caso não tenhamos uma requisição do tipo POST, mas sim uma do tipo request, então
        form = RegisterModelForm # um form limpo será passado para a variável form para ser passado para o contexto

    context = {
        'form': form
    }

    return render(request, 'register.html', context)
