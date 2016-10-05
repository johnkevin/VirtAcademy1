"""
Definition of models.
"""

from django.db import models
from django.conf import settings
from uuid import uuid4
from datetime import date
from django.contrib.auth.models import User
import os
from channels import Group
from django.template.defaultfilters import linebreaks_filter
import json

# Create your models here.


class Facultad (models.Model):
    Cod_Facultad=models.CharField(max_length=2, blank=False, null=False)
    Desc_Facultad=models.CharField(max_length=40, blank=False, null=False)
    email=models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.Desc_Facultad

class Escuela(models.Model):
    facultad=models.ForeignKey(Facultad)
    Desc_Escuela=models.CharField(max_length=40, blank=False, null=False)

    def __str__(self):
        return self.Desc_Escuela

class Condicion(models.Model):
    Desc_Condicion=models.CharField(max_length=40, blank=False, null=False)

    def __str__(self):
        return self.Desc_Condicion

class TipoUsuario(models.Model):
    idTipoUsuario=models.IntegerField(null=False)
    Desc_Tipo=models.CharField(max_length=100,blank=False,null=False)
    def __str__(self):
        return self.Desc_Tipo

class EstadoUsuario(models.Model):
    Desc_Estado=models.CharField(max_length=25, blank=False,null=False)
    def __str__(self):
        return self.Desc_Estado

class PhotoTemp(models.Model):
    def _generar_ruta_image(instance,filename):
        extension = os.path.splitext(filename)[1][1:]
        ruta = os.path.join('{}'.format('files'), date.today().strftime("%Y"))
        #ruta = os.path.join('{}/{}'.format('files',instance.user.username), date.today().strftime("%Y"))
        nombre_archivo = '{}.{}'.format(uuid4().hex, extension)
        return os.path.join(ruta, nombre_archivo)

    user=models.ForeignKey(User)
    phototemp = models.ImageField(upload_to=_generar_ruta_image, blank=True, null=True)

class UserProfile(models.Model):

    def _generar_ruta_imagen(instance,filename):
        extension = os.path.splitext(filename)[1][1:]
        #ruta = os.path.join('{}/{}'.format('profiles',instance.user.username), date.today().strftime("%Y"))
        ruta = os.path.join('{}'.format('profiles'), date.today().strftime("%Y"))
        nombre_archivo = '{}.{}'.format(uuid4().hex, extension)
        return os.path.join(ruta, nombre_archivo)

    user=models.OneToOneField(settings.AUTH_USER_MODEL)
    facultad=models.ForeignKey(Facultad)
    escuela=models.ForeignKey(Escuela)
    condicion=models.ForeignKey(Condicion)
    Tipo=models.ForeignKey(TipoUsuario)
    Nombres=models.CharField(max_length=100, blank=True, null=True)
    ApePat=models.CharField(max_length=40, blank=True, null=True)
    ApeMat=models.CharField(max_length=40, blank=True, null=True)
    fecha_nacimiento=models.DateField(null=True )
    direccion=models.CharField(max_length=100, blank=True, null=True)
    resumen=models.CharField(max_length=300, blank=True, null=True)
    sexo=models.CharField(max_length=1, blank=True, null=True)
    photo = models.ImageField(upload_to=_generar_ruta_imagen, blank=True, null=True)
    estado=models.IntegerField()
    
    def __str__(self):
        return self.user.username
    def fullname(self):
        return (self.ApePat+' '+self.ApeMat+', '+self.Nombres).upper()


class Grado(models.Model):
    Desc_Grado=models.CharField(max_length=40, blank=False, null=False)

    def __str__(self):
        return self.Desc_Grado

class ParamTesistas(models.Model):
    fecha_Inicio=models.DateField(null=False)
    fecha_Fin=models.DateField(null=False)
    cant_minimo=models.IntegerField(null=False)
    cant_maximo=models.IntegerField(null=False)
    observacion=models.CharField(max_length=300,blank=True, null=True)
    estado=models.BooleanField(null=False)
    def __str__(self):
        return "Mínimo: "+self.cant_minimo+" - Máximo: "+self.cant_maximo

class PublicacionTesis(models.Model):
    def _generar_ruta_archivo(instance,filename):
        extension = os.path.splitext(filename)[1][1:]
        #ruta = os.path.join('{}/{}'.format('files',instance.user.username), date.today().strftime("%Y"))
        ruta = os.path.join('{}'.format('files'), date.today().strftime("%Y"))
        nombre_archivo = '{}.{}'.format(uuid4().hex, extension)
        return os.path.join(ruta, nombre_archivo)

    title=models.CharField(max_length=300,blank=False,null=False)
    slug=models.SlugField(max_length=300,editable=False)
    FechaAceptacion=models.DateField(null=False)
    facultad=models.ForeignKey(Facultad)
    escuela=models.ForeignKey(Escuela)
    grado=models.ForeignKey(Grado)
    archivo=models.FileField(upload_to=_generar_ruta_archivo, blank=True, null=True)
    imgVisualizar=models.CharField(max_length=100,blank=False,null=False)
    contenido=models.TextField()
    tags=models.CharField(max_length=300,blank=False,null=False)
    vistas=models.IntegerField()
    create_at = models.DateTimeField(auto_now_add=True)
    userCreate_at=models.ForeignKey(User)

    def __str__(self):
        return self.title

    @property
    def group_name(self):
        return "publicacion-%s" % self.id


class PublicacionTesis_Autor(models.Model):
    publicacion=models.ForeignKey(PublicacionTesis)
    user=models.ForeignKey(User)
    create_at = models.DateTimeField(auto_now_add=True)
    
class PublicacionTesis_Turores(models.Model):
    publicacion=models.ForeignKey(PublicacionTesis)
    user=models.ForeignKey(User)
    create_at = models.DateTimeField(auto_now_add=True)

class PublicacionTesis_Comment(models.Model):
    comentario=models.CharField(max_length=300,blank=False,null=False)
    publicacion=models.ForeignKey(PublicacionTesis)
    user=models.ForeignKey(User)
    create_at=models.DateTimeField(auto_now_add=True)
    estado=models.BooleanField()
    userProfile=models.ForeignKey(UserProfile)

    def html_body(self):
        return self.comentario
        #return linebreaks_filter(self.comentario)

    def send_notification(self):
        notification = {
            "id": self.id,
            "photo":os.path.join('{}').format(self.userProfile.photo),
            "user":self.userProfile.fullname(),
            "codUser":self.user.username,
            "html": self.html_body(),
            "created": self.create_at.strftime("%d %b %Y"),
            "created_hours": self.create_at.strftime("%d-%m-%Y %H:%M:%S"),
        }
        Group(self.publicacion.group_name).send({
            "text": json.dumps(notification),
        })

    def save(self, *args, **kwargs):
        result = super(PublicacionTesis_Comment, self).save(*args, **kwargs)
        self.send_notification()
        return result



class PublicacionTesis_visitas(models.Model):
    publicacion=models.ForeignKey(PublicacionTesis)
    username=models.CharField(max_length=100,blank=False,null=False)
    Desc_User=models.CharField(max_length=300,blank=False,null=False)
    create_at=models.DateTimeField(auto_now_add=True)

#https://vimeo.com/12903891
#http://tutorial-django.readthedocs.io/es/latest/blog/creacion_model.html
#https://keyerror.com/blog/automatically-generating-unique-slugs-in-django
#https://martinpeveri.wordpress.com/2015/02/13/como-trabajar-con-slug-en-la-urls-en-django/
 #slug = models.SlugField(max_length=150, editable=False)
 #from django.utils.text import slugify
 #slug_field_name = 'slug'
 #slug_from = 'name'