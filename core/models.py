from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission  # Preciso dessa biblioteca para fazer
# autenticação, dado que no meu view login_index estou utilizando uma função chamada login na view login_index.
# Precisarei modificar acrescentá-la no meu model register. Estive recebendo um erro, aparentemente, relacionado ao fato
# de estar herdando a classe Base tb, o que estava implicando nas classes Group e Permission que se relacionam com
# AbstractUser. Fiz uma modificação no model Register para eliminar o conflito. POr essa razão, foram importados
from django.contrib.auth.models import User  # Aqui estamos pegando o model User do Django para colocar na variável
# user em Posts, pois, dessa forma, estaremos associando o User logado, especificamente, seu id ao Post

# Temporariamente, estamos removendo os importes abaixo.
# from django.contrib.auth.backends import ModelBackend  # Servirá para criar model abaixo personalizado para
# autenticação de usuários cadastrados com Register
# from django.contrib.auth import get_user_model  # a função pegará o modelo de autenticação atual do projeto - vamos
# definir em settigs.

# SIGNALS
from django.db.models import signals
from django.template.defaultfilters import slugify

# Para lidar com as imagens
from stdimage.models import StdImageField


class Base(models.Model):  # Esses atributos vão estar mais visíveis em admin
    creation = models.DateField('Data de Criação', auto_now_add=True)  # Os dados em string são os nomes que vão
    # aparecer na interface. Assim com os charfields abaixo ou em forms.
    modification = models.DateField('Data de Atualização', auto_now=True)
    active = models.BooleanField('Ativo?', default=True)

    class Meta:
        abstract = True


class Register(AbstractUser):
    """
    # name, email e password que haviamos criado foram removidos, tendo em vista que
    # esse atributos já estão inclusos em AbstractUser. Só precisarei fazer a modificação lá no meu forms para garantir
    # que esse atributos apareçam no meu template.

    Resolvi remover a classe Base, pois com exceção de modification, creation e active são já atributos presentes em
    AbstractUser. Então, apenas acrescentamos abaixo. Mesmo fazendo a remoção de Base, necessitei manter a modificação
    de groups e user_permissions
    """
    username = models.CharField('Nome de usuário', max_length=100, unique=True, blank=False, default="")  # Recebi o
    # erro que diz que necessito fornecer uma valor padrão para que o banco de dados não o coloque
    # como null caso nada seja fornecido. blank = False garente a obrigatoriedade do preenchimento do campo, além do
    # default para não ter o problema de falta de preenchimento.
    modification = models.DateField('Data de Atualização', auto_now=True)
    photo = StdImageField('Imagem', upload_to='registros', variations={'thumb': (124, 124)}, blank=True,
                          default='default_images/default_user.avif')
    # O valor default em photo necessita ser o path para uma imagem, tendo em vista que é isso que StdImageField espera
    # como default
    status = models.CharField('Status', max_length=100, default='Status indefinido!')  # default está em português, pois
    # a frase vai aparecer. Tirei o default="Defina seu status" e coloquei blank == True, pois isso permite que não
    # necessite salvar nada no Status para prosseguir. Voltei atrás e coloquei um default, pois achei que seria mais
    # interessante.
    slug = models.SlugField('Slug', max_length=100, blank=True, editable=False)

    groups = models.ManyToManyField(Group, related_name="user_registers")
    user_permissions = models.ManyToManyField(Permission, related_name="user_registers")

    def __str__(self):
        return self.username


def register_pre_save(signal, instance, sender, **kwargs):
    instance.slug = slugify(instance.username)


signals.pre_save.connect(register_pre_save, sender=Register)


class Post(Base):
    # Um post pertencerá a um usuário, mas um usuário poderá fazer vários posts.
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    user = models.ForeignKey(Register, on_delete=models.CASCADE)  # Haviamos colocado User (importe feito no início do
    # módulo), mas isso estava implicando em view, onde quando queriamos fazer com post.user (esse atributo de post)
    # recebesse como user Register, não estava funcionando, pois ele esperava um objeto do tipo User. Fizemos um código
    # para permitir que isso acontesse, contudo o id que Post estava coletando com models.ForeingKey era o dos usuários
    # , mas o id da base de dados do Django. Isso estava afetando nossa contagem de postagens na view index
    """
    O parâmetro on_delete que é solitado pela função ForeignKey do Django serve para definir o tipo de comportamento
    que devemos ter caso a chave estrangeira seja deletada. Isso ajuda a manter a concistência no banco de dados.
    Temos diferente opções:
    
models.CASCADE: Isso excluirá todas as instâncias relacionadas quando o objeto pai for excluído.
models.PROTECT: Isso impedirá a exclusão do objeto pai se houver objetos filhos relacionados.
models.SET_NULL: Isso definirá o campo de chave estrangeira como NULL para todos os objetos relacionados quando o objeto pai for excluído.
models.SET_DEFAULT: Isso definirá o campo de chave estrangeira como o valor padrão especificado para todos os objetos relacionados quando o objeto pai for excluído.
models.SET(): Isso definirá o campo de chave estrangeira com o valor especificado por uma função personalizada.
models.DO_NOTHING: Isso não fará nada com os objetos relacionados quando o objeto pai for excluído. Isso pode resultar em violações de integridade no banco de dados.
    """
    photo = StdImageField('Imagem', upload_to='posts', variations={'thumb': (124, 124)}, blank=True, default='default_images/default_post.avif')
    title = models.CharField('Título', max_length=100)
    subject = models.CharField('Assunto', max_length=100)
    text = models.TextField('Digite seu texto', max_length=800)
    slug = models.SlugField('Slug', max_length=100, blank=True, editable=False)

    def __str__(self):
        return self.title


def post_pre_save(signal, instance, sender, **kwargs):
    instance.slug = slugify(instance.user.username)  # Fazendo a configuração, garanto que a slug seja criada
    # com base no nome corretamente do autor que a criará a postagem e, consequentemente, sua slug. user é a var em Post
    # username é o atributo que o objeto que o post recebe tem, no caso o objeto é Register que está sendo salvo em
    # user.


signals.pre_save.connect(post_pre_save, sender=Post)

