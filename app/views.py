"""
Definition of views.
"""
#encoding:utf-8
from django.shortcuts import render, redirect, redirect
from django.template import RequestContext
from datetime import datetime
from django.contrib.auth import authenticate, login, login
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, HttpResponseRedirect, Http404
from django.contrib.auth.models import User
from .models import UserProfile, Condicion, Facultad, Escuela,PublicacionTesis
import json
from django.http.response import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from django.views.generic import TemplateView
from django.core import serializers
from django.utils.text import slugify



def home(request):
    """Renders the home page."""
    tesis=PublicacionTesis.objects.filter(title__contains='').select_related('escuela').select_related('facultad').select_related('grado').order_by('FechaAceptacion').values('FechaAceptacion',
                                     'grado__Desc_Grado', 'contenido','escuela__Desc_Escuela', 'facultad__Desc_Facultad','id','imgVisualizar',
                                     'slug', 'tags', 'title').all();
    context={'title':'.:: Bienvenido ::.','year':datetime.now().year,'tesis':tesis}
    return render(request, 'index.html', {'context':context})

def contact(request):
    """Renders the contact page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/contact.html',
        context_instance = RequestContext(request,
        {
            'title':'Contact',
            'message':'Your contact page.',
            'year':datetime.now().year,
        })
    )

def about(request):
    """Renders the about page."""
    assert isinstance(request, HttpRequest)
    return render(
        request,
        'app/about.html',
        context_instance = RequestContext(request,
        {
            'title':'About',
            'message':'Your application description page.',
            'year':datetime.now().year,
        })
    )

def profile(request, username):
    #if request.user.is_authenticated(): 
        _idUser=username      
        userProfile=request.user
        userAppProfile=None
        _valor=True
        _verificarUser=False
        try:
            Usuario=User.objects.get(username=_idUser)
            if Usuario:
                print('si hay usuario')
                if request.user.id==Usuario.id:
                    _verificarUser=True
                try:
                    userAppProfile=UserProfile.objects.get(user=Usuario.id)
                    _valor=True
                except ObjectDoesNotExist:
                    _valor=False
                context={'valor':_valor,'userAppProfile_user':userAppProfile,'title':'Perfil','year':datetime.now().year,"verificarUser":_verificarUser}
                return render(request, 'app/profile.html', {'context':context})
            else:
                print('no hay usuario')
                raise Http404
        except ObjectDoesNotExist:
            raise Http404
    #else:
    #    mensaje=''
    #    return redirect('/login',{'mensaje':mensaje} )
 

def signup(request):

    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        first_name=request.POST['first_name']
        ApelPat=request.POST['ApelPat']
        ApelMat=request.POST['ApelMat']
        _facultad=request.POST['facultad']
        _escuela=request.POST['escuela']
        #condicion=request.POST['condicion']
        last_name=ApelPat+' '+ApelMat
        _mensaje=''
        try:
            if not username:
                _mensaje=_mensaje+"\nIngrese Usuario \n"
            if not password:
                _mensaje=_mensaje+"\nIngrese contraseña \n"
            if not first_name:
                _mensaje=_mensaje+"\nIngrese su nombre \n"
            if not ApelPat:
                _mensaje=_mensaje+"\nIngrese Apellido Paterno \n"
            if not ApelMat:
                _mensaje=_mensaje+"\nIngrese Apellido Materno \n"
            facultad=int(_facultad)
            escuela=int(_escuela)
        except ValueError:
            _mensaje="Ha surgido un error interno, vuelva a intentar el registro"
        if not _mensaje:
            return render(request, 'app/NewUser.html', {'mensaje':'ingreso correcto'})
        else:
            facul=Facultad.objects.all()
            esc=Escuela.objects.filter(facultad_id=facul[0].id)
            context={'mensaje':_mensaje, 'username':username,'password':password,'first_name':first_name,
                     'ApelPat':ApelPat,'ApelMat':ApelMat,'facultad':facul,'escuela': esc,'title':'Registrar Usuario','year':datetime.now().year}
            return render(request, 'app/NewUser.html', {'context':context})
    else:
        facultad=Facultad.objects.all()
        escuela=Escuela.objects.filter(facultad_id=facultad[0].id)
        context = {'facultad':facultad,'escuela': escuela,'year':datetime.now().year}
        return render(request, 'app/NewUser.html', {'context':context})
    return render(request, 'app/NewUser.html', {'mensaje':''})


def setearPassword_user(request):
    mensaje=''
    if request.user.is_authenticated():
        users=User.objects.exclude(id__in=UserProfile.objects.filter().values_list('user'))
        for user in users:
            user.set_password(user.password)
            user.save()
            print(user)
        mensaje='se han filtrado todos los datos'
        return render(request, 'app/changedata.html', {'mensaje': mensaje})
    else:
        mensaje=''
        return render(request, 'app/login.html', {'mensaje': mensaje})




def Login(request):
    if request.user.is_authenticated():
        urlpat='/perfil/'+request.user.username
        return redirect(urlpat, {'title':'Profile'})
    mensaje=''
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']

        if not username:
           if not password:
                mensaje=''
                context={'mensaje':mensaje, 'title':'Inicio de sesión'}
                return render(request, 'app/login.html', {'context':context})
           else:
                mensaje='Ingrese el usuario'
                context={'mensaje':mensaje, 'title':'Inicio de sesión'}
                return render(request, 'app/login.html', {'context':context})
        else:
            if not password:
                mensaje='Ingrese Contraseña'
                context={'mensaje':mensaje, 'title':'Inicio de sesión'}
                return render(request, 'app/login.html', {'context':context})
            else:
                user=None
                try:
                    user=User.objects.get(username=username)
                except ObjectDoesNotExist:
                    print('no hay data')
                if user:
                    print(user.password)
                    if user.password==password:
                        user.set_password(password)
                        user.save()
                    user=authenticate(username=username,password=password)
                    if user is not None:
                        if user.is_active:
                            login(request, user)
                            userProfile=request.user
                            userAppProfile=None
                            _valor=True
                            try:
                                userAppProfile=UserProfile.objects.get(user=request.user.id)
                                _valor=True
                            except ObjectDoesNotExist:
                                _valor=False
                            context={'valor':_valor,'userAppProfile':userAppProfile,'title':'Perfil','year':datetime.now().year}
                            _urlpat='/perfil/'+request.user.username
                            return redirect(_urlpat, {'context':context})
                        else:
                            mensaje='Cuenta inactiva'
                            context={'mensaje':mensaje, 'title':'Inicio de sesión'}
                            return render(request, 'app/login.html', {'context':context})
                else:#verificacion correcta del login
                    user=authenticate(username=username,password=password)
                    if user is not None:
                        if user.is_active:
                            login(request, user)
                            userProfile=request.user
                            userAppProfile=None
                            _valor=True
                            try:
                                userAppProfile=UserProfile.objects.get(user=request.user.id)
                                _valor=True
                            except ObjectDoesNotExist:
                                _valor=False
                            context={'valor':_valor,'userAppProfile':userAppProfile,'title':'Perfil','year':datetime.now().year}
                            _urlpat='/perfil/'+request.user.username
                            return redirect(_urlpat, {'context':context})
                        else:
                            mensaje='Cuenta inactiva'
                            context={'mensaje':mensaje, 'title':'Inicio de sesión'}
                            return render(request, 'app/login.html', {'context':context})
                    else:
                        mensaje='Nombre de usuario o contraseña no válido'
                        context={'mensaje':mensaje, 'title':'Inicio de sesión'}
                        return render(request, 'app/login.html', {'context':context})
    context={'mensaje':mensaje, 'title':'Inicio de sesión',}
    return render(request, 'app/login.html', {'context': context})


def Combo_escuela(request):
    if request.is_ajax()  and request.POST:
        valorFacultad=int(request.POST.get('elegido'))
        escuela= Escuela.objects.filter(facultad_id=valorFacultad).order_by('Desc_Escuela').all()
        _data=''
        for itemescuela in escuela:
            _data=_data+"<option value="+str(itemescuela.id)+">"+itemescuela.Desc_Escuela+"</option>"
        data=json.dumps(_data)        
        return HttpResponse(data, content_type='application/json')
    else:
        raise Http404
    
    
def busquedaEscuelas(request):
    if request.is_ajax()  and request.GET:
        valFacultad= int(request.GET['facultad'])
        escuelas= Escuela.objects.filter(facultad_id=valFacultad).order_by('Desc_Escuela').all()
        if escuelas:
            data=serializers.serialize('json', escuelas, fields= ('pk','Desc_Escuela'))
        else:
            data=[]
        return HttpResponse(data, content_type='application/json')
    else:
        raise Http404
    

def ChangeProfile(request):
    if request.user.is_authenticated():
            userProfile=request.user
            userAppProfile=None
            facultad=None
            escuela=None
            condicion=None
            _valor=False
            IdFacultad=0
            IdEscuela=0
            IdCondicion=0
            percent=0
            try:
                userAppProfile=UserProfile.objects.get(user=request.user.id)
                _valor=True
                IdFacultad=userAppProfile.facultad_id
                condicion=Condicion.objects.all().order_by('Desc_Condicion')
            except ObjectDoesNotExist:
                _valor=False
            try:
                facultad=Facultad.objects.all().order_by('Desc_Facultad')
                #condicion=Condicion.objects.all().order_by('Desc_Condicion')
                if _valor:
                    IdEscuela=userAppProfile.escuela_id
                    escuela=Escuela.objects.filter(facultad_id=IdFacultad).order_by('Desc_Escuela').all()
                    IdCondicion=userAppProfile.condicion_id
                    percent=CalcularPorcentajePerfil(userAppProfile)
                else:
                    escuela=Escuela.objects.filter(facultad_id=facultad[0].id).order_by('Desc_Escuela').all()
            except ObjectDoesNotExist:
                print('error...')
            context={'valor':_valor,'userAppProfile':userAppProfile,'facultad':facultad,
                     'escuela':escuela,'condicion':condicion,'IdFacultad':IdFacultad,
                     'IdEscuela':IdEscuela,'IdCondicion':IdCondicion,'percent':percent,}
            return render(request, 'app/PerfilUserModifcacion.html', {'context':context})
    else:
        mensaje=''
        return render(request, 'app/login.html', {'mensaje': mensaje})
        #return redirect('/login',{'mensaje':mensaje} )



def CalcularPorcentajePerfil(objeto):
    _Percent=0
    try:
        if objeto.Nombres:
            _Percent=_Percent+5
        if objeto.ApePat:
            _Percent=_Percent+5
        if objeto.ApeMat:
            _Percent=_Percent+5
        if objeto.direccion:
            _Percent=_Percent+10
        if objeto.fecha_nacimiento:
            _Percent=_Percent+5
        if objeto.sexo:
            _Percent=_Percent+5
        if objeto.photo:
            _Percent=_Percent+20
        if objeto.facultad_id:
            _Percent=_Percent+10
        if objeto.escuela_id:
            _Percent=_Percent+10
        if objeto.condicion_id:
            _Percent=_Percent+10
        if objeto.resumen:
            _Percent=_Percent+15
    except ValueError:
        print('Error de conversiones')
    return _Percent


def CambiarPerfilData(request):
    mensaje=''
    if request.user.is_authenticated():
        if request.is_ajax() and request.POST:
            val=False
            try:
                _facultad= int(request.POST.get('facultad'))
                _escuela= int(request.POST.get('escuela'))
                _condicion= int(request.POST.get('condicion'))
                formato_fecha = "%d-%m-%Y"
                _FechaNacimiento=datetime.strptime(request.POST.get('form-field-date'),formato_fecha).date()
                _nombreUser=request.POST.get('username').capitalize()
                _ApePat=request.POST.get('ApePat').capitalize()
                _ApeMat=request.POST.get('ApeMat').capitalize()
                _Direccion=request.POST.get('direction').capitalize()
                _ExtractoProfesional= request.POST.get('Extracto').capitalize()
                _sexo=request.POST.get('form-field-radio')
                _apellidos='%s%s'%(_ApePat,_ApeMat)
                mensaje='a'
            except ValueError:
                mensaje=''
            if not mensaje.strip:
                mensaje='Error inesperado, vuelva a ejecutar otra vez'
                data={'msj':mensaje,'valor': val,'percent':0}
                return HttpResponse(json.dumps(data), content_type='application/json')
            else:
                _percent=0
                try:
                    Usuario=request.user
                    Usuario.first_name=_nombreUser
                    Usuario.last_name=_apellidos
                    Usuario.save()
                    request.user=Usuario
                    UsuarioPerfil=UserProfile.objects.get(user=request.user.id)
                    if UsuarioPerfil:
                        #Facultad_data=Facultad.objects.get(id=_facultad)
                        #Escuelta_data=Escuela.objects.get(id=_escuela)
                        #Condicion_data=Condicion.objects.get(id=_condicion)
                        #UsuarioPerfil.facultad=Facultad_data
                        UsuarioPerfil.facultad_id=_facultad
                        UsuarioPerfil.escuela_id=_escuela
                        UsuarioPerfil.condicion_id=_condicion
                        #UsuarioPerfil.escuela=Escuelta_data
                        #UsuarioPerfil.condicion=Condicion_data
                        UsuarioPerfil.Nombres=_nombreUser
                        UsuarioPerfil.ApePat=_ApePat
                        UsuarioPerfil.ApeMat=_ApeMat
                        UsuarioPerfil.fecha_nacimiento=_FechaNacimiento
                        UsuarioPerfil.direccion=_Direccion
                        UsuarioPerfil.resumen=_ExtractoProfesional
                        UsuarioPerfil.sexo=_sexo
                        UsuarioPerfil.save()
                    val=True
                    _percent=CalcularPorcentajePerfil(UsuarioPerfil)
                    mensaje='Los datos han sido modificados correctamente'
                except:
                    mensaje='Error inesperado, al momento de modificar los datos'
                    val=False
                    _percent=0
                data={'msj':mensaje,'valor': val,'percent':_percent}
                return HttpResponse(json.dumps(data), content_type='application/json')
        else:
            raise Http404
    else:
        mensaje=''
        return render(request, 'app/login.html', {'mensaje': mensaje})

def CambiarContrasenia(request):
    mensaje=''
    if request.user.is_authenticated():
        if request.is_ajax()  and request.POST and request.user.is_authenticated():
            ContraAct=request.POST.get('ContActual')
            ContraNew=request.POST.get('ContNueva')
            ContraEqual=request.POST.get('ConfCont')
            _mensaje=''
            if not ContraAct:
                _mensaje=_mensaje+"* Ingrese Contraseña Actual  <br/>"
            if not ContraNew:
                _mensaje=_mensaje+"* Ingrese Contraseña Nueva  <br/>"
            if not ContraEqual:
                _mensaje=_mensaje+"* Ingrese confirmación de Contraseña <br/>"
            if _mensaje:
                data=_mensaje
                return HttpResponse(json.dumps(data), content_type='application/json')
            else:
                if ContraNew ==ContraEqual:
                    if User.check_password(request.user,ContraAct):
                        usuario= User.objects.get(id=request.user.id)
                        usuario.set_password(ContraNew)
                        usuario.save()
                        data="La contraseña ha sido modificada"
                        request.user=usuario
                    else:
                        data="La contraseña actual es incorrecta"
                else:
                    data="La contraseña nueva con la confirmación son incorrectas"
                return HttpResponse(json.dumps(data), content_type='application/json')
        else:
            raise Http404
    else:
        mensaje=''
        return render(request, 'app/login.html', {'mensaje': mensaje})
    
def CambiarEstadoUsuario (request):
    mensaje=''
    if request.user.is_authenticated():
        if request.is_ajax()  and request.POST:
            valEstado=request.POST.get('estado').upper()
            valEstado_ante=request.POST.get('esta_ant').upper()
            clas1=''
            clas2=''
            valor1=False
            var_estado=1
            if valEstado_ante=="DISPONIBLE":
                clas1='ace-icon fa fa-circle light-green'
                valor1=True
            elif valEstado_ante=="OCUPADO":
                clas1='ace-icon fa fa-circle light-red'
                valor1=True
            elif valEstado_ante=="INVISIBLE":
                clas1='ace-icon fa fa-circle light-grey'
                valor1=True

            if valEstado=="DISPONIBLE":
                clas2='ace-icon fa fa-circle light-green'
                var_estado=1
                valor2=True
            elif valEstado=="OCUPADO":
                clas2='ace-icon fa fa-circle light-red'
                var_estado=2
                valor2=True
            elif valEstado=="INVISIBLE":
                clas2='ace-icon fa fa-circle light-grey' 
                var_estado=3
                valor2=True

            try:
                if valor1 and valor2:
                    userAppProfile=UserProfile.objects.get(user=request.user.id)
                    userAppProfile.estado=var_estado
                    userAppProfile.save()
            except ObjectDoesNotExist:
                print('error interno')

            data={'clas1':clas1,'clas2':clas2,'valor1':valor1, 'valor2':valor2, 'etiqueta':valEstado}
            return HttpResponse(json.dumps(data), content_type='application/json')
        else:
            raise Http404
    else:
        mensaje=''
        return render(request, 'app/login.html', {'mensaje': mensaje})
