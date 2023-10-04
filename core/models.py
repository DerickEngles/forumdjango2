from django.db import models
from stdimage.models import StdImageField

# SIGNALS
from django.db.models import signals
from django.template.defaultfilters import slugify


class Base(models.Model):  # Esses atributos vão estar mais visíveis em admin
    creation = models.DateField('Data de Criação', auto_now_add=True)  # Os dados em string são os nomes que vão
    # aparecer na interface. Assim com os charfields abaixo ou em forms.
    modification = models.DateField('Data de Atualização', auto_now=True)
    active = models.BooleanField('Ativo?', default=True)

    class Meta:
        abstract = True


class Register(Base):
    photo = StdImageField('Imagem', upload_to='registros', variations={'thumb': (124, 124)})
    name = models.CharField('Nome', max_length=100)
    status = models.CharField('Status', max_length=100, default='Status indefinido!')  # default está em português, pois
    # a frase vai aparecer. Tirei o default="Defina seu status" e coloquei blank == True, pois isso permite que não
    # necessite salvar nada no Status para prosseguir. Voltei atrás e coloquei um default, pois achei que seria mais
    # interessante.
    slug = models.SlugField('Slug', max_length=100, blank=True, editable=False)

    def __str__(self):
        return self.name


def register_pre_save(signal, instance, sender, **kwargs):
    instance.slug = slugify(instance.name)


signals.pre_save.connect(register_pre_save, sender=Register)
