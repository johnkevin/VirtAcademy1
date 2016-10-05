"""
Definition of urls for VirtAcademy.
"""

from datetime import datetime
from django.conf.urls import patterns, url, include
from app.forms import BootstrapAuthenticationForm
from app.profiles.urls import urlpatterns
from django.conf import settings
from django.contrib.auth.decorators import login_required

# Uncomment the next lines to enable the admin:
# from django.conf.urls import include
from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    url(r'^$', 'app.views.home', name='home'),
    url(r'^contact$', 'app.views.contact', name='contact'),
    url(r'^NewUser', 'app.views.signup', name='NewUser'),
    url(r'^about', 'app.views.about', name='about'),
    url(r'^perfil/(?P<username>[-\w]+)/$', 'app.views.profile', name='profile'),
    url(r'^ChangeProfile', 'app.views.ChangeProfile', name='ChangeProfile'),
    url(r'^buscarEscuelas', 'app.views.busquedaEscuelas', name='buscarEscuelas'),
    url(r'^changedata', 'app.views.setearPassword_user', name='changedata'),

    url(r'^ajax/CambiarContrasenia', 'app.views.CambiarContrasenia'),
    url(r'^CambiarPerfilData', 'app.views.CambiarPerfilData', name='CambiarPerfilData'),
    url(r'^ajax/CambiarEstado', 'app.views.CambiarEstadoUsuario'),
    
    url(r'^ajax/Comments', 'app.profiles.views.Comentar', name='Comentario'),
    #url(r'^tesis/registro/(?P<registro>[-\w]+)/$','app.profiles.views.tesispublicadas', name="tesispublicadas"),
#    url(r'^actas/actas_municipales/$',login_required(actas_municipales), name="actas_municipales"),
	

    url(r'^SearchRegParamTesis', 'app.profiles.views.ConsultarDataParamTesistas'),

    url(r'^Tesis/listado/$','app.profiles.views.tesispublicadas', name="tesispublicadas"),
    url(r'^Tesis/UploadTesis', 'app.profiles.views.registrarTesis'),
    url(r'^Tesis/RegParamTesis$', 'app.profiles.views.Registro_ParamFechaTesis'),
    url(r'^Tesis/Registrar', 'app.profiles.views.prueba_other', name='registrarTesis'),
    url(r'^Tesis/uploadImagetemp$', 'app.profiles.views.SubirImagenTemporal', name='uploadImagetemp'),
    url(r'^Tesis/Publicacion/(?P<slug>[-\w]+)/$', 'app.profiles.views.VisualizarTesis', name='tesispublicacion'),
    url(r'^Tesis/Registro/(?P<id>[-\w]+)/$', 'app.views.profile', name='tesisregistro'),

    url(r'^ajax/saveRegParamTesis', 'app.profiles.views.saveRegParamTesis'),
    url(r'^delRegParamTesis', 'app.profiles.views.deleteRegParamTesis'),
    url(r'^buscarParamRegistro', 'app.profiles.views.busquedaDataregistro'),
    url(r'^consfecha', 'app.profiles.views.consultarMinMaxTesistas'),     
    url(r'^filtrarPersona$', 'app.profiles.views.busquedaPersonas'),
    url(r'^uploadImage$', 'app.profiles.views.subirImagenPerfil', name='uploadImage'),
    url(r'^other$', 'app.profiles.views.home_other', name='other'),
    url(r'^login$', 'app.views.Login', name='Login'),
    url(r'^ajax', 'app.views.Combo_escuela'),
    url(r'^logout$',
        'django.contrib.auth.views.logout',
        {
            'next_page': '/',
        },
        name='logout'),
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
        'document_root': settings.MEDIA_ROOT
    }),
    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
     url(r'^admin/', include(admin.site.urls)),
)
