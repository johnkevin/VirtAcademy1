# Create your views here.
#encoding:utf-8

from django.shortcuts import render, redirect, redirect
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponseRedirect, Http404
from datetime import datetime
from django.http.response import HttpResponse
from django.http import HttpRequest, HttpResponseRedirect, Http404
from django.core import serializers
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from app.models import Escuela, Facultad, Grado, UserProfile,ParamTesistas,PhotoTemp,PublicacionTesis,PublicacionTesis_Autor,PublicacionTesis_Turores,PublicacionTesis_Comment
import json
from django.db.models import Q
from uuid import uuid4
import os
from VirtAcademy.settings import MEDIA_ROOT, PROJECT_ROOT, ROOT_URLCONF, WSGI_APPLICATION, MEDIA_URL
from django.contrib.sites.models import Site
from django.template.defaultfilters import slugify
import sys


def home_other(request):
    if request.user.is_authenticated() and request.method=='GET' : 
        """Renders the home page."""
        facultad=Facultad.objects.all()
        escuela=Escuela.objects.filter(facultad_id=facultad[0].id)
        grados=Grado.objects.all()
        context={'title':'.:: Registro Tesis ::.','year':datetime.now().year,'facultad':facultad,
                             'escuela':escuela,'grados':grados}
        return render(request, 'archive/SubirArchivo.html', {'context':context})
    else:
        return redirect('/login',{'mensaje':''} )

def prueba_other(request):
    if request.user.is_authenticated(): 
        facultad=Facultad.objects.all()
        escuela=Escuela.objects.filter(facultad_id=facultad[0].id)
        grados=Grado.objects.all()
        context={'title':'.:: Registro Tesis ::.','year':datetime.now().year,'facultad':facultad,'escuela':escuela,'grados':grados}
        return render(request, 'archive/UploadFile.html', {'context':context})
    else:
        return redirect('/login',{'mensaje':''} )



def Registro_ParamFechaTesis(request):
    if request.user.is_authenticated():
        parametroTesis=ParamTesistas.objects.filter(estado=False).order_by('-fecha_Inicio')
        fechaActual=datetime.now()
        context={'parametroTesis':parametroTesis,'title':'.:: Parametro Tesis ::.','year':datetime.now().year,'fechaActual':fechaActual}
        return render(request, 'archive/RegistroParamTesis.html', {'context':context})
    else:
        return redirect('/login',{'mensaje':''} )

def ConsultarDataParamTesistas(request):
    mensaje=''
    if request.user.is_authenticated():
        if request.is_ajax() and request.POST:
            try:
                _isTodos=request.POST.get('stateChecked')
                parametroTesis=None
                if _isTodos=='true':
                    parametroTesis=ParamTesistas.objects.filter(estado=False).order_by('-fecha_Inicio').all()
                else:
                    formato_fecha = "%d-%m-%Y"
                    _FechaInicio=datetime.strptime(request.POST.get('fechaInicio'),formato_fecha).date()
                    _FechaFin=datetime.strptime(request.POST.get('fechaFin'),formato_fecha).date()
                    parametroTesis=ParamTesistas.objects.filter((Q(fecha_Inicio__range=(_FechaInicio,_FechaFin))|
                                                                Q(fecha_Fin__range=(_FechaInicio,_FechaFin))), estado=False).order_by('-fecha_Inicio').all()
                data=serializers.serialize('json', parametroTesis, fields=('pk','fecha_Inicio','fecha_Fin','cant_minimo','cant_maximo','observacion'))
            except:
                data=[]
            return HttpResponse(data, content_type='application/json')
        else:
            raise Http404
    else:
        return render(request, 'app/login.html', {'mensaje': ''})


def busquedaPersonas(request):
    if request.is_ajax()  and request.POST:
        cadenaBusqueda=request.POST.get('data[q]')
        personas=User.objects.filter(Q(username__startswith=cadenaBusqueda)| 
                                     Q(first_name__startswith=cadenaBusqueda)|
                                                    Q(last_name__startswith=cadenaBusqueda)).order_by('last_name')[:10]
        data_primary=[]
        data_ultimate={}
        if personas:
            for objectPersona in personas:
                data_auxiliar={}
                #data_auxiliar['text']=objectPersona.username.upper()+" : "+objectPersona.last_name.upper()+", "+objectPersona.first_name.upper()
                data_auxiliar['text']=objectPersona.last_name.upper()+", "+objectPersona.first_name.upper()
                data_auxiliar['id']=objectPersona.username
                data_primary.append(data_auxiliar)
        data_ultimate['results']=data_primary
        data_ultimate['q']=cadenaBusqueda
        return HttpResponse(json.dumps(data_ultimate), content_type='application/json')
    else:
        raise Http404
    
def subirImagenPerfil(request):
    if request.is_ajax() and request.POST:
        result=[]
        result_aux={}
        try:
            image_perfil=request.FILES['avatar']
            PerfilUser=UserProfile.objects.get(user_id=request.user.id)
            PerfilUser.photo=image_perfil
            PerfilUser.save()
            _urlImage=PerfilUser.photo
            #_rutaImagen=os.path.join('{}{}{}'.format(request.META['HTTP_HOST'],MEDIA_URL,_urlImage))
            _rutaImagen=os.path.join('{}{}'.format(MEDIA_URL,_urlImage))
            result_aux['status'] = "OK"
            result_aux['message']="Avatar ha sido cambiado satisfactoriamente"
            result_aux['url']=_rutaImagen
        except :
            result_aux['status'] = "ERR"
            result_aux['message']="Ha ocurrido un error intentando actualizar Avatar"
        result.append(result_aux)
        return HttpResponse(json.dumps(result),content_type='application/json')
    else:
        raise Http404

def SubirImagenTemporal(request):
    if request.POST:
        result=[]
        result_aux={}
        try:
            image_perfil=request.FILES['image']
            phototemp=PhotoTemp(phototemp=image_perfil,user=request.user)
            phototemp.save()            
            _urlImage=phototemp.phototemp
            _urlImagetemp=os.path.join('{}').format(_urlImage)
            _rutaImagen=os.path.join('{}{}'.format(MEDIA_URL,_urlImage))
            result_aux['status'] = "OK"
            result_aux['url']=_rutaImagen
            result_aux['urlimage']=_urlImagetemp
        except ValueError:
            result_aux['status'] = "ERR"
        result.append(result_aux)
        return HttpResponse(json.dumps(result),content_type='application/json')
    else:
        raise Http404
    
def deleteRegParamTesis(request):
    if request.user.is_authenticated():
        if request.is_ajax() and request.POST:
            try:
                idpk_registro=int(request.POST.get('pkRegistro'))
            except:
                data={'valor':1,'mensaje':'Ha ocurrido un error en el envio de la información'}
                return HttpResponse(json.dumps(data), content_type='application/json')
            try:
                paramTesis=ParamTesistas.objects.get(id=idpk_registro, estado=False)
                paramTesis.estado=True
                paramTesis.save()
                #paramTesis.delete()
                data={'valor':0,'mensaje':''}
                return HttpResponse(json.dumps(data), content_type='application/json')
            except:
                data={'valor':1,'mensaje':'Ha ocurrido un error interno, intentelo otra vez'}
                return HttpResponse(json.dumps(data), content_type='application/json')
        else:
            raise Http404
    else:
        return render(request, 'app/login.html', {'mensaje': mensaje})

def saveRegParamTesis(request):
    if request.user.is_authenticated():
        if request.is_ajax() and request.POST:
            try:
                idpk_registro= request.POST.get('pkRegistro')
                formato_fecha = "%d-%m-%Y"
                _FechaInicio=datetime.strptime(request.POST.get('form_field_dateIn'),formato_fecha).date()
                _FechaFin=datetime.strptime(request.POST.get('form_field_dateFn'),formato_fecha).date()
                _CantMinimo=int(request.POST.get('spinner1'))
                _CantMaxima=int(request.POST.get('spinner2'))
                _Observacion=request.POST.get('observacion')
            except:
                data={'valor':1,'mensaje':'Ha ocurrido un error en el envio de la información'}
                return HttpResponse(json.dumps(data), content_type='application/json')
            
            if idpk_registro: #Modificar
                try:
                    _idpk_registro=int(idpk_registro)
                    paramTesis=ParamTesistas.objects.get(id=_idpk_registro, estado=False)
                    if(paramTesis):
                        paramTesis.fecha_Inicio=_FechaInicio
                        paramTesis.fecha_Fin=_FechaFin
                        paramTesis.cant_minimo=_CantMinimo
                        paramTesis.cant_maximo=_CantMaxima
                        paramTesis.observacion=_Observacion
                        paramTesis.save()
                        data={'valor':0,'mensaje':''}
                        return HttpResponse(json.dumps(data), content_type='application/json')
                    else:
                        data={'valor':1,'mensaje':'Ha ocurrido un error interno, intentelo otra vez'}
                        return HttpResponse(json.dumps(data), content_type='application/json')
                except:
                    data={'valor':1,'mensaje':'Ha ocurrido un error interno, intentelo otra vez'}
                    return HttpResponse(json.dumps(data), content_type='application/json')
            else: #Nuevo
                try:
                    regParamTesis=ParamTesistas(fecha_Inicio=_FechaInicio,fecha_Fin=_FechaFin,cant_minimo=_CantMinimo,cant_maximo=_CantMaxima,observacion=_Observacion,estado=False)
                    regParamTesis.save()
                    data={'valor':0,'mensaje':''}
                    return HttpResponse(json.dumps(data), content_type='application/json')
                except:
                    data={'valor':1,'mensaje':'Ha ocurrido un error interno, intentelo otra vez'}
                    return HttpResponse(json.dumps(data), content_type='application/json')
        else:
            raise Http404
    else:
        return render(request, 'app/login.html', {'mensaje': ''})


def busquedaDataregistro(request):
    if request.user.is_authenticated():
        if request.is_ajax()  and request.POST:
            try:
                idpk_registro= int(request.POST.get('IdReg'))
                #idpk_registro= int(request.GET['IdReg'])
                print(idpk_registro)
                paramTesis=ParamTesistas.objects.get(id=idpk_registro, estado=False)
                fechaIn=str(paramTesis.fecha_Inicio)
                fechaFn=str(paramTesis.fecha_Fin)
                cantminimo=paramTesis.cant_minimo
                cantmaximo=paramTesis.cant_maximo
                observacion=''
                if paramTesis.observacion:
                    observacion=paramTesis.observacion
                data={'valor':0, 'mensaje':'','fechaIn':fechaIn,
                      'fechaFn':fechaFn,'cantminimo':cantminimo,'cantmaximo':cantmaximo,'observacion':observacion}
                return HttpResponse(json.dumps(data), content_type='application/json')
            except:
                data={'valor':1, 'mensaje':'Error al consultar los datos','fechaIn':'','fechaFn':'','cantminimo':'','cantmaximo':'','observacion':''}
                return HttpResponse(json.dumps(data), content_type='application/json')
        else:
            raise Http404
    else:
        return render(request, 'app/login.html', {'mensaje': ''})

def consultarMinMaxTesistas(request):
    if request.user.is_authenticated():
        if request.is_ajax() and request.POST:
            try:
                formato_fecha = "%d-%m-%Y"
                _FechaConsulta=datetime.strptime(request.POST.get('form_field_date'),formato_fecha).date()
            except:
                data={'valor':1, 'mensaje':'Error al consultar los datos','CantMin':0,'CantMax':0}                
                return HttpResponse(json.dumps(data), content_type='application/json')

            try:
                #paramTesis=ParamTesistas.objects.filter(fecha_Inicio__lte=_FechaConsulta,fecha_Fin__gte=_FechaConsulta, estado=False)
                paramTesis=ParamTesistas.objects.get(fecha_Inicio__lte=_FechaConsulta,fecha_Fin__gte=_FechaConsulta, estado=False)
                #print(paramTesis.fecha_Inicio)
                
                #paramTesis=ParamTesistas.objects.get(Q(fecha_Inicio__year__lte=_year),Q(fecha_Inicio__month__lte=_month),
                #                                     Q(fecha_Inicio__day__lte=_day),Q(fecha_Fin__year__gte=_year),
                #                                     Q(fecha_Fin__month__gte=_month),Q(fecha_Fin__day__gte=_day),estado=False)
                
                #data={'valor':0, 'mensaje':'No se ha encontrado parámetros establecidos para la fecha indicada','CantMin':'','CantMax':''}
                data={'valor':0, 'mensaje':'','CantMin':paramTesis.cant_minimo,'CantMax':paramTesis.cant_maximo}
                return HttpResponse(json.dumps(data), content_type='application/json')
            except Exception as inst:
                data={'valor':1, 'mensaje':'No se ha encontrado parámetros establecidos para la fecha indicada','CantMin':0,'CantMax':0}
                return HttpResponse(json.dumps(data), content_type='application/json')
        else:
            raise Http404
    else:
        return render(request, 'app/login.html', {'mensaje': ''})


def registrarTesis(request):
    if request.user.is_authenticated():
        mensaje=''
        _valor=False
        if request.is_ajax() and request.POST:
            try:
                _facultad= int(request.POST.get('facultad'))
                _escuela=int(request.POST.get('escuela'))
                _grado=int(request.POST.get('grado'))
                _archivopdf=request.FILES['id_input_file_3']
                _urlimage=request.POST.get('urlimage')
                _tags=request.POST.get('form_field_tags')
                _tituloTesis=request.POST.get('titulotesis')
                formato_fecha = "%d-%m-%Y"
                _FechaAprobacion=datetime.strptime(request.POST.get('form_field_date'),formato_fecha).date()
                _tesistas=request.POST.get('IdTesistas')
                _tutores=request.POST.get('IdTutores')
                _contenido=request.POST.get('iseditor')
                _idtesistas=_tesistas.split(",")
                _idtutores=_tutores.split(",")                                 
                mensaje=''
                _valor=True
            except ValueError:
                _valor=False
            try:
                if _valor:
                    if _idtesistas:
                        tempPublicacionTesis=PublicacionTesis(title=_tituloTesis,slug=slugify(_tituloTesis),FechaAceptacion=_FechaAprobacion,
                                                                  facultad_id=_facultad,escuela_id=_escuela,grado_id=_grado,archivo=_archivopdf,
                                                                  imgVisualizar=_urlimage,contenido=_contenido,tags=_tags,vistas=0,userCreate_at=request.user)
                        tempPublicacionTesis.save()  
                                                
                        for dt in _idtesistas:
                            tesista=User.objects.get(username=dt)
                            if tesista:
                                tempPublicacionTesistas=PublicacionTesis_Autor(publicacion=tempPublicacionTesis,user=tesista)
                                tempPublicacionTesistas.save()

                        for dt in _idtutores:
                            tutor=User.objects.get(username=dt)
                            if tutor:
                                tempPublicacionTutores=PublicacionTesis_Turores(publicacion=tempPublicacionTesis,user=tutor)
                                tempPublicacionTutores.save()
                        data={'valor':0,'mensaje':'','redirect':'listado'}
                    else:
                        data={'valor':1,'mensaje':'no se ha encontrado tesistas','redirect':''}
                else:
                    data={'valor':1,'mensaje':'Error al leer la información','redirect':''}
            except ValueError:
                print(ValueError)
                data={'valor':1,'mensaje':'Error al intentar guardar la información','redirect':''}
            return HttpResponse(json.dumps(data), content_type='application/json')
        else:
            raise Http404
    else:
        return render(request, 'app/login.html', {'mensaje': ''})


def tesispublicadas(request):
    if request.user.is_authenticated():
        #if request.method=='GET':             
        pagina=request.GET.get('pagina')
        cadenaBusqueda=request.GET.get('search')
        if not cadenaBusqueda:
            cadenaBusqueda=''
        tesis=PublicacionTesis.objects.filter(userCreate_at=request.user,title__contains=cadenaBusqueda).select_related('escuela').select_related('facultad').select_related('grado').order_by('FechaAceptacion').values('FechaAceptacion',
                                     'grado__Desc_Grado', 'contenido','escuela__Desc_Escuela', 'facultad__Desc_Facultad','id','imgVisualizar',
                                     'slug', 'tags', 'title').all()
        paginador=Paginator(tesis,10)
        try:
            tesis=paginador.page(pagina)
        except PageNotAnInteger:
            tesis=paginador.page(1)
        except EmptyPage:
            tesis=paginador.page(paginador.num_pages)
        context={'tesis':tesis,'cadenaBusqueda':cadenaBusqueda}
        return render(request, 'archive/ListadoArchivos.html', context)
        #else: 
         #   raise Http404
    else:
        return redirect('/login',{'mensaje':''})

def VisualizarTesis(request,slug):
    _slug=slug
    if _slug:
        _valor=True
        try:
            tesis=PublicacionTesis.objects.select_related('escuela').select_related('facultad').select_related('grado').get(slug=_slug)
            autores=PublicacionTesis_Autor.objects.filter(publicacion_id=tesis.id).select_related('user').values('id','user__username','user__first_name','user__last_name').all()
            tutores=PublicacionTesis_Turores.objects.filter(publicacion_id=tesis.id).select_related('user').values('id','user__username','user__first_name','user__last_name').all()
            comentarios=PublicacionTesis_Comment.objects.filter(publicacion_id=tesis.id).select_related('userProfile').select_related('user').values('id','comentario',
                    'create_at','userProfile__id','userProfile__Nombres','userProfile__ApePat','userProfile__ApeMat','userProfile__photo','userProfile__sexo','user__username').order_by('-create_at').all()
            profiles=None 
            try:
                profiles=UserProfile.objects.get(user=request.user)
            except:
                profiles=None
                    #'userProfile__sexo','user__username').all()
            #PublicacionTesis.objects.filter(id=tesis.id).update(vistas=F('vistas')+1)
                        
            context={'title':'Tesis','year':datetime.now().year,'tesis':tesis,'autores':autores,'tutores':tutores,#,
                     'comentarios':comentarios,'profile':profiles}
            return render(request, 'archive/visualizador.html', {'context':context})
        except:
            _valor=False
            raise Http404
    else:
        raise Http404

def Comentar(request):
    if request.is_ajax():
        print('1')
        pkregistro=request.POST.get('pkRegistro')
        optiontext='registrar'
        optionvalue=0
        if pkregistro:
            print('2')
            optiontext='modificar'
            optionvalue=1
        if request.user.is_authenticated():
            print('3')
            if request.POST and request.user.is_authenticated():
                print('4')
                Comentario=request.POST.get('Comment')
                if Comentario:
                    print('5')
                    try:
                        if pkregistro:
                            print('6')
                            try:
                                objectComments=PublicacionTesis_Comment.objects.get(id=int(pkregistro),estado=False)
                                if objectComments.user==request.user:
                                    print('7')
                                    objectComments.comentario=Comentario
                                    objectComments.save()
                                    data={
                                        'option':'0',
                                        'valor':optionvalue,
                                        'mensaje':'Comentario modificado correctamente'
                                        }
                                    return HttpResponse(json.dumps(data), content_type='application/json')
                                else:
                                    data={
                                        'option':'6',
                                        'valor':optionvalue,
                                        'mensaje':'No puede '+optiontext+' este comentario'
                                        }
                                    return HttpResponse(json.dumps(data), content_type='application/json')
                            except:
                                data={
                                        'option':'5',
                                        'valor':optionvalue,
                                        'mensaje':'ha ocurrido un error al intentar '+optiontext+' el comentario'
                                        }
                                return HttpResponse(json.dumps(data), content_type='application/json')
                        else:
                            idtesis=request.POST.get('idtesis')
                            userAppProfile=UserProfile.objects.get(user=request.user.id)
                            tempComments=PublicacionTesis_Comment(comentario=Comentario,publicacion_id=idtesis,user=request.user,
                                              estado=False,userProfile=userAppProfile)
                            tempComments.save() 
                            data={
                                'option':'0',
                                'valor':optionvalue,
                                'mensaje':'Comentario guardado correctamente'
                                }
                            return HttpResponse(json.dumps(data), content_type='application/json')
                    except:
                        data={
                            'option':'4',
                            'valor':optionvalue,
                            'mensaje':'ha ocurrido un error al intentar '+optiontext+' el comentario'
                            }
                        return HttpResponse(json.dumps(data), content_type='application/json')
                else:
                    data={
                        'option':'3',
                        'valor':optionvalue,
                        'mensaje':'Escribe un comentario...'
                        }
                    return HttpResponse(json.dumps(data), content_type='application/json')
            else:
                data={
                        'option':'2',
                        'valor':optionvalue,
                        'mensaje':'Ha ocurrido un error al intentar '+optiontext+' el comentario'
                        }
                return HttpResponse(json.dumps(data), content_type='application/json')
        else:
            data={
                'option':'1',
                'valor':optionvalue,
                'mensaje':'Asegúrese de loguearse para poder realizar un comentario'
                }
            return HttpResponse(json.dumps(data), content_type='application/json')
    else:
        Http404

#http://pvilas.com/2011/02/consultas-en-django.html
#def busquedaregistrotesis(request, registro):
#    if request.user.is_authenticated(): 
#        try:
#        except:
#    else:
#       return redirect('/login',{'mensaje':''} )


    #{{context.valor_prueba|safe}}