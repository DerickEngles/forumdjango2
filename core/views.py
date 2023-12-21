from django.shortcuts import render, redirect
from django.contrib import messages  # Esse messages está vindo do meu contato.html
from django.contrib.auth import login, authenticate, update_session_auth_hash # Vamos usar o authenticate para
# autenticar um usuário que se registrar
# ou seja, quando houver um redirect para index, o usuário já constará como logado.
# update_session_auth_hash - Servirá atualizar a sessão e manter o usuário que fez a alteração de dados logado


# Função responsável por criar uma sessão para o usuário. As sessões vão salvando
# dados do usuário, dados de navegação que facilitam o acesso do usuário e o processamento daquilo que ele faz dentro
# de um site, como o carrinho de compras em um ecommerce (as informações são salvar nas sessions). POr isso, em nosso
# projeto conseguimos acessar os dados do usuário no meu projeto, com request.user em certas views
from django.contrib.auth.decorators import login_required # decorator para ser colocado em uma página que desejo
# que o acesso seja feito apenas por usuário logados. Será útil para view postagens
from django.contrib.auth.models import User

# OS forms são importados para que nosso templates tenham uma aparência e os models para termos acesso aos dados do
# banco de dados

from .forms import MessageForm, RegisterModelForm, PostModelForm, UserDataChangeModelForm, RecoverDatasForm, \
    UpdatePostModelForm

from .models import Register, Post  # O model Register vai trazer os dados diretamente do banco de dados para minha
# via index

from django.http import HttpResponseRedirect
from django.urls import reverse


def index(request):
    users = User.objects.all()
    # username = request.user.username - Removi, pois eu estava querendo que o usuário que se registrar fosse realizada
    # uma alteração no navbar, o que não estava acontecendo antes. Isso foi feito quando o autenticamos além de
    # registrá-lo em register.
    print(f'Dentro do index view: {request.user.username}')
    registers = Register.objects.all()
    posts = Post.objects.all()  # Estou salvando todos os posts na variável vindo do banco
    user_post_counts = {}  # dict que vai salvar a quantidade de posts de cada usuário
    # count = 0
    """
    for user in users:
        count = sum(1 for post in posts if post.user == user)  # Estou contabilizando os posts de cada usuário
        user_post_counts[user.id] = count  # e vou salvando no dict. Criamos o dict para salvar os valores de forma
        # individualizada, onde poderia acessar com base em register.id dos register que passaremos para index
        # no context

    context = {
        'registers': registers,
        'users': users,  # Não conseguimos acesso direto a users em index. Acredito pq estamos a acessando em um bloco
        # de código específico
        'user_post_counts': user_post_counts
    }
    """
    for register in registers:
        count = sum(1 for post in posts if post.user_id == register.id)  # Estou contabilizando os posts de cada usuário
        user_post_counts[register.id] = count  # e vou salvando no dict. Criamos o dict para salvar os valores de forma
        # individualizada, onde poderia acessar com base em register.id dos register que passaremos para index
        # no context

    context = {  # é a forma como HTML recebe dados - é uma espécie de arquivo JSON
        'registers': registers,
        'user_post_counts': user_post_counts
    }

    return render(request, 'index.html', context)


def register(request):
    # print(request.user)  # para saber o tipo de usuário que acessa a página registro. Um AnonymousUser consegue aces
    # sar. No caso desse nosso progrma deve ser desse jeito, pois quero cadastrar diferentes usuários.
    if str(request.method) == 'POST':
        form = RegisterModelForm(request.POST, request.FILES)  # variável que vai salvar os dados que vierem request
        # POST (inseridos no Template) e request.Files será um diretório com imagens
        if form.is_valid():  # is_valid é uma das funções de form - O formulário é válido se ele tem dados, se os dados
            # são do tipo especificado lá no form (lembrando que alguns do dados vão para o banco de dados, o que signi
            # fica que estão configurados no models) e algum validação personalizada
            username = form.cleaned_data['username']
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            # Essa busca por e-mail vai fazer com que só seja possível cadastrar um usuário por e-mail. Poderiamos
            # resolver esse problema também definindo nosso e-mail como unique no Model Register
            user_django = User.objects.filter(email=email).first()  # Fará a busca no database do Django
            user_database = Register.objects.filter(email=email).first()  # Fará a busca no MySQL

            if user_django or user_database:
                messages.error(request, 'Já existe um usuário cadastrado com o e-mail fornecido!')
                form = RegisterModelForm()  # para passarmos um model limpo para à página após erro
            else:
                user_save = User.objects.create_user(username=username, email=email, password=password)  # para salvar n
                # base de dados do Django. Era isso que estava faltando para conseguir me autenticar com o usuário
                # Agora ele está sendo salvo na base de dados do Django e não mais apenas no banco de dados.
                form.save()  # para salvar no banco de dados
            # form = RegisterModelForm() Garantindo que o template receba um novo form limpo para o cadastrado de novo
            # usuário para ser passado para o contexto. Contudo quero algo diferente: que o usuário seja direcionado
            # para a página principal
                user = authenticate(username=username, password=password)  # A função authenticate verifica se as
                # credenciais fornecidas pelo usuário correspondem a um usuário registrado no banco de  dados. Se as
                # credenciais estiverem corretas, ele retorna um objeto de usuário. Se não, retorna None.
                if user is not None:
                    messages.success(request, f'Usuário cadastrado e logado com sucesso! Bem-vindo {username}')
                    # Removi o message de cima ao ter o salvamento de usuário para não ser redundante e para salientar
                    # que ele está logado no sistema
                    login(request, user)
                    # A função login(request, user) é usada para iniciar uma sessão para o usuário no sistema. Ela é
                    # usada após a autenticação bem-sucedida, ou seja, se houver um user.
                else:
                    messages.error(request, 'Erro ao autenticar/logar o usuário!')  # Caso seja none, isto é, não seja
                    # retornado um user do database do Django, essa mensagem é exibida
                return redirect('index')  # A posição de index garante que o usuário seja redirecionado para index com
            # ou sem login
        else:
            messages.error(request, 'Erro ao cadastrar usuário, pois o formulário não é válido!')
    else:  # Caso não tenhamos uma requisição do tipo POST, mas sim uma do tipo request, então
        form = RegisterModelForm()  # um form limpo será passado para a variável form para ser passado para o contexto
        # caso o tipo de request nao seja POST

    context = {
        'form': form
    }

    return render(request, 'register.html', context)

"""
ESSA VIEW É DESNECESSÁRIA, TENDO EM VISTA QUE O DJANGO JÁ POSSUI UMA VIEW PARA AUTENTICAÇÃO EMBUTIDA, BASTANDO APENAS
QUE FAÇAMOS O IMPORT DELA EM VIEWS

def login_index(request):  # vai ver se há algum usuário com aquele e-mail e senha
    if str(request.method) == 'POST':  # O tipo de requisição é POST, pois o usuário vai enviar dados pelo FORM -
        # nçao confuda ser POST com o ato de salvar dados no banco de dados, pois toda ação de envio de dados pelo HTML
        # é um tipo POST.
        form = LoginForm(request.POST)  # Vai conter o e-mail e a senha digitados pelo usuário
        if form.is_valid():
            email = form.cleaned_data['email']  # O cleaned_data tem a função de formatar os dados que vem do form HTML
            # colocando esses dados em um formato correto para serem processados aqui no back_end
            password = form.cleaned_data['password']
            user = Register.objects.filter(email=email, password=password).first()  # Aqui vamos checar se o e-mail e
            # senha digitados na página estão no banco de dados e faço isso através do meu model Register.
            
            Quando você usa filter() em um modelo no Django, ele retorna um queryset, que é uma coleção de objetos que 
            atendem aos critérios especificados na consulta. No seu caso, você está usando o método filter() para 
            encontrar um usuário com um determinado email e senha. A chamada ao método filter() não retorna o objeto 
            em si, mas sim um queryset contendo todos os objetos que atendem aos critérios de filtro.

A função first() é usada para extrair o primeiro objeto do queryset retornado pelo filter(). Se não houver nenhum 
objeto que atenda aos critérios de filtro, first() retornará None. Se houver um ou mais objetos que atendam aos 
critérios, first() retornará o primeiro objeto desse conjunto.

No seu caso, ao usar first() após o filter(), você está buscando o primeiro objeto que atende aos critérios de filtro 
específicos. Se o objeto existir, será atribuído à variável user. Se não existir, user será None.
            

            if user is not None:
                print(f'Print DENTRO DE LOGIN: {user}')
                login(request, user)
                messages.success(request, 'Logado com sucesso!')
                
                Conseguimos ter a exibição do nome do usuário logado no template, mas ainda está errado dessa forma, 
                pois continuamos na rota login e quando clicamos para voltar para index, não temos a continuidade do login
                
                if request.user.is_authenticated:
                    username = request.user.username

                    context = {
                        'registers': Register.objects.all(),
                        'username': username
                    }

                    return render(request, 'index.html', context)
                return redirect('index')
            else:
                messages.error(request, 'Dados incorretos ou usuário não cadastrado')
                form = LoginForm()  # Garante um form limpo ao ocorrer erro
        else:
            messages.error(request, 'Erro! Dados inválidos')
    else:  # Se a requisição for diferente de POST, como GET, apenas acesso a página
        form = LoginForm()  # passe um formulário limpo para à página

    context = {  # variável que vai passar para a tela o form
        'form': form
    }

    return render(request, 'login.html', context)
"""


def message(request):
    print(f'Print DENTRO DE MESSAGE{request.user}')
    username = request.user.username

    form = MessageForm(request.POST or None)  # O formulário pode ter dados ou estar vazio (usualmente, quando
    # o usuário abrir a página apenas, teremos um form do tipo None.
    if str(request.method) == 'POST':
        if form.is_valid():  # Função da classe Form
            form.send_email()  # função que criamos na nossa classe forms
    # Vou precisar checar se o método é do tipo POST ou
            messages.success(request, 'Mensagem enviada com sucesso!')
            form = MessageForm()  # Estamos passando o formulário vazio
        else:
            messages.error(request, 'Erro ao enviar mensagem!')
    else:  # Passando um form limpo para caso o request seja um get
        form = MessageForm()

    context = {  # Garante que seja passado para o HTML um forms com aparência/campos que foram criados em forms
        'form': form
    }
    return render(request, 'contact.html', context)
    # else:
    #    return redirect('index')


@login_required()
def userdatachange(request):
    print(f'Usuário logado e acessando à página de alteração de dados: {request.user}')
    if str(request.method) == 'POST':
        form = UserDataChangeModelForm(request.POST, request.FILES)
        if form.is_valid():
            # Vamos coletar os dados, pois precisaremos salvar no database do Django
            new_username = form.cleaned_data['username']
            new_email = form.cleaned_data['email']
            new_password = form.cleaned_data['password']
            new_status = form.cleaned_data['status']
            new_photo = form.cleaned_data['photo']
            print(f'Primeiro print de new{new_photo}')
            # Vamos coletar os usuário do database do Django e do MySQL que desejamos fazer a alteração
            user_django = User.objects.filter(email=new_email).first()
            user_database = Register.objects.filter(email=new_email).first()
            print(f'Primeiro print da foto no database {user_database.photo}')
            if not user_django and not user_database:
                messages.error(request, 'Erro ao tentar encontrar usuário')
                form = UserDataChangeModelForm()
            else:
                user_django.username = new_username
                user_django.email = new_email
                user_django.set_password(new_password)
                user_django.save()

                # Executando o salvamento no MySQL - EU TENHO TODOS OS DADOS QUE PRECISO SALVAR NO MYSQL EM FORM. TEREI
                # TERIA UMA FORMA MAIS DIRETA DE FAZER ISSO SEM SER UM POR UM??? O CHATGPT DISSE QUE NÃO HÁ. PRECISO
                # FAZER O SALVAMENTO INDIVIDUAL
                user_database.username = new_username
                user_database.email = new_email
                user_database.password = new_password
                user_database.status = new_status
                if new_photo == "default_images/default_user.avif":
                    user_database.photo = user_database.photo
                else:
                    user_database.photo = new_photo
                user_database.save()  # Havia faltado o enctype no HTML

                # Com a mudança de dados, precisamos atualizar a sessão para manter o usuário logado
                update_session_auth_hash(request, user_django)
                # Após isso, vamos redirecioná-lo para index com uma mensagem de sucesso
                messages.success(request, 'Dados atualizados com sucesso!')
                return redirect('index')
        else:
            messages.error(request, 'Erro ao tentar alterar dados!')

    else:  # Ao entrar na página sempre terei um request GET, ou seja, dados será exibidos na página, como de forms ou
        # , no caso, os dados do usuário vindos do banco de dados:
        user_database = Register.objects.filter(email=request.user.email).first()
        if user_database:
            initial_data = {  # Data para preencher o atributo initial explicado abaixo
                'username': user_database.username,
                'email': user_database.email,
                'password': user_database.password,
                'status': user_database.status,
                'photo': user_database.photo
            }
            form = UserDataChangeModelForm(initial=initial_data)  # forms, classe pai de form, conforme definido em forms.py,
            # tem, indiretamente (não é dele diretamente - averiguamos com o shell), um atributo initial para definir
            # informações/para que realizemos um pré-preenchimento, que será feito para não termos que ter os usuário
            # preenchendo todos os dados todas às vezes que só desejarem alterar um específico

    context = {
        'form': form
    }

    return render(request, 'user_data_change.html', context)


def recoverdata(request):
    form = RecoverDatasForm(request.POST or None)

    if str(request.method) == 'POST':
        if form.is_valid():
            email = form.cleaned_data['email']
            user_django = User.objects.filter(email=email).first()

            if user_django:
                form.send_email()
                messages.success(request, 'Mensagem enviada com sucesso!')
                return redirect('index')  # Será redirecionado para a rota index
            else:
                messages.error(request, 'Usuário não encontrado ou e-mail incorreto!')
                form = RecoverDatasForm()
        else:
            messages.error(request, 'Erro ao enviar mensagem!')
    else:
        form = RecoverDatasForm()

    context = {
            'form': form
        }

    return render(request, 'recoverdata.html', context)


def post(request):
    username = request.user.username
    print(f'Dentro do index view: {request.user.username}')
    context = {
        'posts': Post.objects.all()  # Ele não reconhece, mas conseguiremos usar. PQ?? Pq pode ser um falso negativo
        # da IDE ou algum tipo de configuração que está exibindo o não reconhecimento do método objects para Post.
        # Todo model, possui esse método. Nosso Model Post não é um Model que foi criado através de um Model do próprio
        # Django como é o caso de Register, que tenha AbstractUser como model pai. O model pai de Post é Base, model
        # criado por nós. Então, ele, provavelmente, gerá essa mensagem por conta disso. Contudo Post tem uma form de
        # model. Então, ele é gerado como Model.
    }

    return render(request, 'posts.html', context)


@login_required()
def creatpost(request):
    user_database = Register.objects.filter(email=request.user.email).first()  # Estamos coletando o objeto do tipo
    # Register pelo email do user (conseguimos fazer esse request, pois temos o usuário autenticado pelo model do Django
    # se há um user autenticado, então, conseguimos coletar dados dele. Fizemos isso, pois vamos passar para o user,
    # atributo de Post definido em model, em prol de passar como foreign key a key/id desse Register (id do banco de
    # dados, pois, dessa forma, conseguimos vincular esse usuário logado ao Post em post.user = user_database. Na
    # realidade, não estamos passando dados do usuário logado, estamos utilizado os dados dele (no caso o e-mail) para
    # pesquisar o registro dele no banco de dados MySQL, pois é o id desse registro que queremos vincular ao Poste, em
    # prol de fazer a lógica de contagem de Posts funcionar.

    if str(request.method) == 'POST':
        form = PostModelForm(request.POST, request.FILES)

        if form.is_valid():
            # Para que não seja dado erro, antes de comitar/salvar o post no banco de dados, necessito passar o usuário
            # logado para ele. Quando fizemos a modificação no Model, estamos consigo
            post = form.save(commit=False)  # Ele será salvo na base de dados do Django, mas não no banco. Por isso,
            # commit False. Fazer isso nos garante poder fazer modificações, como as seguinte antes do comite


            # Será que devo passar o id do user. Acho que sim, pois isso que sinalizei para ter no banco de dados, o
            # id do usuário

            # post.user = request.user  # Estamos adicionando ao post, variável que contém nosso forms, o usuário logado
            # print(f'O request.user {request.user}')
            # print(f'O user_database.id {user_database.id} e nome {user_database.username}')
            post.user = user_database # Em model, ele vai coletar o id do user que buscamos em Register através do email
            # conforme variável na primeira linha dessa função. Isso será feito em model através da função foregin key
            post.save()  # Por fim, realizamos o salvamento.
            messages.success(request, 'Postagem realizada com sucesso!')
            return redirect('posts')
        else:
            messages.error(request, 'Erro ao realizar a postagem!')
            form = PostModelForm()
    else: # Get
        form = PostModelForm()

    context = {
        'form': form
    }

    return render(request, 'creat_post.html', context)


@login_required()
def deletepost(request, post_id):
    post = Post.objects.filter(id=post_id)
    if post:
        post.delete()
        messages.success(request, 'Postagem deletada com sucesso!')
    else:
        messages.error(request, 'Erro ao excluir postagem!')

    return redirect('posts')


@login_required()
def updatepost(request, post_id):
    post = Post.objects.get(id=post_id)
    if str(request.method) == 'POST':
        form = UpdatePostModelForm(request.POST, request.FILES)
        if form.is_valid():
            new_title = form.cleaned_data['title']
            new_subject = form.cleaned_data['subject']
            new_text = form.cleaned_data['text']
            new_photo = form.cleaned_data['photo']

            # post = Post.objects.get(id=post_id)  # Não preciso utilizar first(), pois estou pesquisando, diretamente,
            # pelo id do post e sendo ele uma primary key única

            if post:
                post.title = new_title
                post.subject = new_subject
                post.text = new_text

                if new_photo == 'default_images/default_post.avif':
                    post.photo = post.photo
                else:  # Significa que ele recebeu uma nova foto - lembre-se que ele muda para default quando não recebe
                    # nenhuma foto como é o caso acima
                    post.photo = new_photo

                messages.success(request, 'Postagem atualizada com sucesso!')
                post.save()
                return redirect('posts')
            else:
                messages.error(request, 'Erro ao localizar a postagem!')

        else:
            messages.error(request, 'Não foi possível atualizar a postagem!')
            form = UpdatePostModelForm()
    else:
        if post:
            initial_data = {
                'title': post.title,
                'subject': post.subject,
                'text': post.text,
                'photo': post.photo
            }
            form = UpdatePostModelForm(initial=initial_data)  # forms, classe pai de form, conforme definido em
            # forms.py, tem, indiretamente (não é dele diretamente - averiguamos com o shell), um atributo initial para
            # definir informações/para um pré-preenchimento, que será feito para não termos que ter os usuário
            # preenchendo todos os dados todas às vezes que só desejarem alterar um específico

    context = {
        'form': form,
        'post': post
    }
    return render(request, 'updatepost.html', context)

"""
View Update post do chatgpt

@login_required()
def updatepost(request, post_id):
    try:
        post = Post.objects.get(id=post_id)
    except Post.DoesNotExist:
        messages.error(request, 'Postagem não encontrada!')
        return redirect('post')

    if request.method == 'POST':
        form = UpdatePostModelForm(request.POST, request.FILES, instance=post) # instance=post serve para sinalizar
        os dados para o pré-preenchimento desse form.
        if form.is_valid():
            form.save()
            messages.success(request, 'Postagem atualizada com sucesso!')
            return redirect('post')
        else:
            messages.error(request, 'Não foi possível atualizar a postagem!')
    else:
        form = UpdatePostModelForm(instance=post)

    context = {
        'form': form
    }
    return render(request, 'updatepost.html', context)
"""


"""
Diferença no uso do filter e get nas consultas dos Posts nas duas últimas views:

Em Django, filter() e get() são métodos de consulta diferentes.

filter() retorna um queryset que pode conter zero, um ou vários resultados, mesmo que apenas um objeto corresponda ao 
filtro. Ele sempre retorna uma lista de resultados, mesmo que possa conter apenas um objeto.

get() retorna um único objeto que corresponda aos critérios fornecidos na consulta. Se mais de um objeto corresponder 
aos critérios ou nenhum objeto corresponder, ele lançará uma exceção DoesNotExist ou MultipleObjectsReturned.

No caso da função deletepost, você usou filter() para buscar os posts com base no id fornecido. Isso retorna um 
queryset, e você executou o método delete() diretamente nesse queryset, que deleta todos os objetos dentro do queryset.

Por outro lado, na função updatepost, você está buscando um post específico pelo id usando get(). Isso é apropriado 
quando você espera obter um único objeto e precisa trabalhar com ele. No caso de get(), se nenhum objeto for encontrado 
com o id fornecido, ele levantará uma exceção DoesNotExist, e é por isso que muitas vezes é usado em situações em que 
você espera exatamente um objeto para ser retornado.

Em resumo, a escolha entre filter() e get() depende do que você está tentando alcançar: filter() para buscar vários 
objetos que correspondem a um critério e get() para buscar um único objeto específico com base em um critério único e 
esperado.

Poderia ter feito a consulta em updatepost, usando filter, como :post = Post.objects.filter(id=post_id).first()
"""