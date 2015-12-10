from django.shortcuts import render
from django.shortcuts import render_to_response
from django.template import RequestContext
from contable.forms import UserCreationForm,EmpleadoForm
from contable.models import Empleado,Puesto,Cuenta,TipoCuenta,Transaccion, TipoMonto, Transacciones, EstadoPeriodo, Comprobacion

from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect
from django.core.context_processors import csrf
from django.contrib.auth.models import User , Group, Permission
import time
util=0
haber=0
capContable=0
user = User()
cerrar = EstadoPeriodo()

# Create your views here.

@login_required(login_url='/ingresar')
def inicio(request):
    global user
    return render(request,'index.html', {'usuario' : user.get_username()})

@login_required(login_url='/ingresar')
def planillaEmpleados(request):
    e=Empleado.objects.all()
    p=Puesto.objects.all()
    emp=Empleado()
    pue=Puesto()
    if request.method=='POST':
        he=request.POST['horasExtras']
        cod=request.POST['codigo']
        emp1=Empleado.objects.get(id=cod)
        p1=Puesto.objects.get(id=emp1.puesto_id)
        emp1.horasExtras=he
        emp1.salDevengado=round((float(he)*p1.pHoraExtra)+p1.salBase,2)
        emp1.isss=round(emp1.salDevengado*0.075,2)
        emp1.afp=round(emp1.salDevengado*0.0675,2)
        if emp1.salDevengado>338.67:
            emp1.renta=round(emp1.salDevengado*0.0083333,2)
        emp1.salPagar = round(emp1.salDevengado-emp1.isss-emp1.afp-emp1.renta,2)
        emp1.save()
    return render(request, 'planilla-empleados.html', {'empleado':e, 'puesto':p, 'num' : len(e)})

@login_required(login_url='/ingresar')
def catalogoCuentas(request):
    return render(request, 'catalogo-cuentas.html', {'cuentas':Cuenta.objects.order_by('tipoCuenta_id'), 'tipoCuenta':TipoCuenta.objects.all()})

def ingresar(request):
    global user
    if not request.user.is_anonymous():
        return HttpResponseRedirect('../index')
    if request.method=='POST':
        formulario = AuthenticationForm(request.POST)
        if formulario.is_valid:
            usuario = request.POST['username']
            clave = request.POST['password']
            user = User.objects.get(username = usuario)
            acceso = authenticate(username=usuario, password=clave)
            if acceso is not None:
                if acceso.is_active:
                    login(request,acceso)
                    return HttpResponseRedirect('../index')
                else:
                    return render_to_response('noactivo.html',context_instance=RequestContext(request))
            else:
                return render_to_response('nousuario.html', context_instance=RequestContext(request))
    else:
        formulario = AuthenticationForm()
    return render_to_response('ingresar.html',{'formulario':formulario}, context_instance=RequestContext(request))
# global usuarios

@login_required(login_url='/ingresar')
def nuevo_usuario(request):
    global user
    if user.has_perm('contable.add_empleado') == False:
        return render(request ,'error.html',{'mensaje':'No posee permisos', 'link':'/index'})

    if request.method=='POST':
        formulario=UserCreationForm(request.POST)
        if formulario.is_valid():# and (clave1 == clave2):
            formulario.save()
            
            return HttpResponseRedirect('/index')
    else:
        formulario=UserCreationForm()
    return render_to_response('nuevousuario.html',{'formulario':formulario}, context_instance=RequestContext(request))


@login_required(login_url='/ingresar')
def cerrar(request):
	logout(request)
	return HttpResponseRedirect('/ingresar')

@login_required(login_url='/ingresar')
def ingresar_empleado(request):
    global user
    if user.has_perm('contable.add_empleado') == False:
        return render(request ,'error.html',{'mensaje':"No tiene permisos", 'link':'/index'})

    if request.POST:
        empForm=EmpleadoForm(request.POST)
        if empForm.is_valid():
            c=request.POST['Puesto']
            if (c=="0"):
                return HttpResponseRedirect('/empleado')
            else:
                p = Empleado()
                m = Puesto()
                p.nombre = request.POST['nombre']
                p.apellido = request.POST['apellido']
                p.horasExtras = 0
                p.isss=0
                p.afp=0
                p.renta=0
                p.salDevengado=0
                p.salPagar=0
                p.dui = request.POST['dui']
                p.nit = request.POST['nit']
                m=Puesto.objects.get(id=c)
                p.puesto = m
                p.save()
                return HttpResponseRedirect('/index')
    else:
        empForm=EmpleadoForm()
    args={}
    args.update(csrf(request))
    args['empForm'] = empForm
    return render_to_response('registrar_empleado.html',args)

@login_required(login_url='/ingresar')
def ingresar_cuenta(request):
    global user
    if user.has_perm('contable.add_cuenta') == False:
        return render(request ,'error.html',{'mensaje':"No tiene permisos", 'link':'/index'})

    if request.method == 'GET':
        return render(request ,'registrar_cuenta.html', {'tipo':TipoCuenta.objects.all()})
    if request.POST:
        c=request.POST['Cuenta']
        if (c=="0"):
            return HttpResponseRedirect('/cuenta')
        else:
            a = Cuenta()
            s = TipoCuenta()
            a.nom_cuenta = request.POST['nom_cuenta']
            a.saldo = 0
            s=TipoCuenta.objects.get(id=c)
            a.tipoCuenta = s
            cod = ''
            if c == '1':
                cod = 'A0'
            elif c == '2':
                cod = 'P0'
            elif c == '3':
                cod = 'C0'
            elif c == '4':
                cod = 'R0'
            
            cod = cod + str(len(Cuenta.objects.all()) + 1)
            a.codigo = cod
            a.montoCargo=0
            a.montoAbono=0
            a.save()
            return HttpResponseRedirect('/index')
    return render(request,'registrar_cuenta.html')

@login_required(login_url='/ingresar')
def transaccion(request):
    global user
    if user.has_perm('contable.add_transaccion') == False:
        return render(request ,'error.html',{'mensaje':"No tiene permisos", 'link':'/index'})

    if request.method == "GET":
        return render(request ,'form-transaccion.html', {'cuentas':Cuenta.objects.all()})

    if request.method=="POST":
        count=int(request.POST['counter'])
        i=1
        l=1
        montoCa=0
        montoAb=0
        for k in range(count):
            var1='cuenta'+str(l)
            var2='monto'+str(l)
            if (request.POST[var2]) == '':
                mont=0
            else:
                mont=float(request.POST[var2])
            cuent=int(request.POST[var1])
            if cuent!=0:
                if l%2==0: #es abono
                    montoAb=montoAb+mont
                else:
                    montoCa=montoCa+mont
            l=l+1
        t=Transacciones.objects.all()
        num=0
        for h in t:
            num = int(h.numero)
        num = num + 1
        if montoCa==montoAb: #partida doble
            for j in range(count):
                var1='cuenta'+str(i)
                cuent=int(request.POST[var1])
                if cuent!=0:
                    c=Cuenta()
                    tr = Transacciones()
                    var1='cuenta'+str(i)
                    var2='monto'+str(i)
                    monto=float(request.POST[var2])
                    c=Cuenta.objects.get(id=request.POST[var1])
                    tm1=TipoMonto.objects.get(id=1)
                    tm2=TipoMonto.objects.get(id=2)
                    #t.monto=monto
                    tr.cuenta=c
                    tr.numero=num
                    tr.fecha=time.strftime("%x")
                    if i%2==0:
                        #t.tipoMonto=tm2  #es abono
                        c.montoAbono=c.montoAbono+monto
                        tr.abono=monto
                        tr.cargo=0
                    else:
                        tr.cargo=monto   #es cargo
                        tr.abono=0
                        c.montoCargo=c.montoCargo+monto
                    c.saldo = c.montoCargo - c.montoAbono
                    c.save()
                    tr.save()
                i=i+1
        else:
            m = "No se cumple partida doble"
            r = '/transaccion'
            return  render(request ,'error.html', {'mensaje' : m})
        return HttpResponseRedirect('/index')
    else:
        return HttpResponseRedirect('/transaccion')

@login_required(login_url='/ingresar')
def eliminar_emp(request):
    global user
    if user.has_perm('contable.delete_empleado') == False:
        return render(request ,'error.html',{'mensaje':"No tiene permisos", 'link':'/index'})

    if request.method == 'GET':
        return render(request ,'eliminar_empleado.html', {'eliminar':Empleado.objects.all()})
    if request.method=="POST":
        ele=Empleado.objects.get(id=request.POST['eliminar'])
        ele.delete()
        return HttpResponseRedirect('/index')
    else:
        return HttpResponseRedirect('/eliminar')

@login_required(login_url='/ingresar')
def comprobacion(request):
    global user
    
    per = EstadoPeriodo.objects.filter(periodoActivo = True)
    if len(per) != 0:
        return render(request ,'error.html',{'mensaje':"No se ha cerrado periodo contable", 'link':'/index'})
    
    c=Cuenta.objects.order_by('tipoCuenta_id')
    tm1=TipoMonto.objects.get(id=1)
    tm2=TipoMonto.objects.get(id=2)
    trans = Transaccion.objects.all()
    monto1 = 0
    monto2 = 0
    p = EstadoPeriodo()
    for periodo in per:
        p = periodo
    for t in trans:
        t.delete()
    for cuenta in c:
        comp=Comprobacion()
        tran=Transaccion()
        monto=float(cuenta.saldo)
        if monto<0:
            tran.monto=monto*(-1)
            tran.tipoMonto=tm2
            tran.cuenta=cuenta
            monto=monto*-1
            monto2 = monto2 + monto
            comp.nombreCuenta=cuenta.nom_cuenta
            comp.debe=monto
            comp.haber=0
        else:
            tran.monto=monto
            tran.cuenta=cuenta
            tran.tipoMonto=tm1
            monto1 = monto1 + monto
            comp.nombreCuenta=cuenta.nom_cuenta
            comp.haber=monto
            comp.debe=0
        tran.save()
        comp.estadoPeriodo_id=28
        comprobando=Comprobacion.objects.all()
        for co in comprobando:
            if  comp.nombreCuenta == co.nombreCuenta:
                comp.estadoPeriodo_id=co.estadoPeriodo_id
                comp.debe=co.debe
                comp.haber=co.haber
                comp.id=co.id
        comp.save()
        trans = Transaccion.objects.all()
    return render(request, 'comprobacion.html', {'transaccion':trans,'cuenta':c, 'm1': monto1, 'm2': monto2})

@login_required(login_url='/ingresar')
def resultado(request):
    per = EstadoPeriodo.objects.filter(periodoActivo = True)
    if len(per) != 0:
        return render(request ,'error.html',{'mensaje':"No se ha cerrado periodo contable", 'link':'/index'})
    c=Cuenta.objects.filter(tipoCuenta=4)
    t=Transaccion.objects.all()
    global util
    global haber
    util = 0
    for cuenta in c :
        util = util + cuenta.saldo
    if util < 0:
        util = util * -1
        haber = 1
    else:
        haber = 2
    return render(request,'resultado.html',{'transaccion':t,'cuenta':c, 'saldo' : util, 'haber' : haber})

@login_required(login_url='/ingresar')
def capital(request):
    global util
    global haber
    global capContable
    capContable=0.0
    if util == 0:
        return HttpResponseRedirect('resultado')
    c=Cuenta.objects.filter(tipoCuenta=3)
    t=Transaccion.objects.all()
    for cuenta in c :
        capContable=capContable+cuenta.saldo
    if capContable<0:
        capContable=capContable*-1

    if haber==1:
            capContable=capContable + util
            haberc = 1
    elif haber==2:
            capContable=capContable - util
            haberc = 2

    return render(request,'capital.html',{'transaccion':t,'cuenta':c, 'util':util,'haber':haber,'haberc':haberc,'cap':capContable})

@login_required(login_url='/ingresar')
def general(request):
    global capContable
    global haber
    if capContable == 0:
        return HttpResponseRedirect('/capital')
    monto1=0
    monto2=0
    t=Transaccion.objects.all()
    c1=Cuenta.objects.filter(tipoCuenta=1)
    c2=Cuenta.objects.filter(tipoCuenta=2)
    for cuenta1 in c1:
        monto1=monto1+cuenta1.saldo
    for cuenta2 in c2:
        monto2=monto2-cuenta2.saldo
    monto2=monto2+capContable

    return render(request,'general.html',{'cap':capContable,'activos':c1,'pasivos':c2,'cargo':monto1,'abono':monto2,'transaccion':t,'haber':haber})

@login_required(login_url='/ingresar')
def libroDiario(request):
    return render(request, 'libroDiario.html', {'transaccion':Transacciones.objects.all(), 'cuenta':Cuenta.objects.all()})

@login_required(login_url='/ingresar')
def ajustes(request):
    global user
    
    if user.has_perm('contable.add_estadoperiodo') == False:
        return render(request ,'error.html',{'mensaje':"No tiene permisos", 'link' : "/index"})
    
    per = EstadoPeriodo.objects.filter(periodoActivo = True)
    if len(per) != 0:
        return render(request ,'error.html',{'mensaje':"No se ha cerrado periodo contable", 'link':'/index'})
    
    if request.method == 'POST':
        per = len(EstadoPeriodo.objects.all())
        txt = request.POST['cod']
        txt2 = "{% extends 'base.html' %}{% block static %}<link               rel='stylesheet'href='../static/css/tabla.css'>{% endblock %}{% block titulo %}Periodo{% endblock %}{% block menu %}{% include 'menu.html' %}{% endblock %}{% block contenido %}"
        archi = open('contable\plantillas\periodo\periodo'+str(per)+'.html', 'w')
        archi.write(txt2)
        archi.write(txt.encode('utf-8'))
        archi.write("{% endblock %}")
        archi.close()
        return HttpResponseRedirect('/index')
    
    comp=Comprobacion.objects.all()
    monto1=0
    monto2=0
    for c in comp:
        monto1=monto1+c.debe
        monto2=monto2+c.haber

    c=Cuenta.objects.order_by('tipoCuenta_id')
    tm1=TipoMonto.objects.get(id=1)
    tm2=TipoMonto.objects.get(id=2)
    trans = Transaccion.objects.all()
    monto3 = 0
    monto4 = 0
    for t in trans:
        t.delete()
    for cuenta in c:
        tran=Transaccion()
        monto=float(cuenta.saldo)
        if monto<0:
            tran.monto=monto*(-1)
            tran.tipoMonto=tm2
            tran.cuenta=cuenta
            monto4 = monto4 + monto*(-1)
        else:
            tran.monto=monto
            tran.cuenta=cuenta
            tran.tipoMonto=tm1
            monto3 = monto3 + monto
        tran.save()
    #estado de resultados
    resultados=Cuenta.objects.filter(tipoCuenta=4)
    utilidad = 0
    for cuenta in resultados :
        utilidad = utilidad + cuenta.saldo
    if utilidad < 0:
        utilidad = utilidad * -1
        habere = 1
    else:
        habere = 2
    #estado de capital
    global capContable
    capContable=0.0
    capitales=Cuenta.objects.filter(tipoCuenta=3)
    for cuenta in capitales :
        capContable=capContable+cuenta.saldo
    if capContable<0:
        capContable=capContable*-1

    if habere==1:
            capContable=capContable + utilidad
            haberca = 1
    elif habere==2:
            capContable=capContable - utilidad
            haberca = 2
    #balance general
    monto5=0
    monto6=0
    c1=Cuenta.objects.filter(tipoCuenta=1)
    c2=Cuenta.objects.filter(tipoCuenta=2)
    for cuenta1 in c1:
        monto5=monto5+cuenta1.saldo
    for cuenta2 in c2:
        monto6=monto6-cuenta2.saldo
    monto6=monto6+capContable

    return render(request,'ajustes.html', {'transaccion':trans,'cuenta':c, 'comprobacion':comp,'cuenta':c, 'm1': monto1, 'm2': monto2,'m3':monto3,'m4':monto4,'resultados':resultados,'saldo' : utilidad,'habere' :habere, 'capitales':capitales,'haberca':haberca,'cap':capContable,'activos':c1,'pasivos':c2,'cargo':monto5,'abono':monto6})


@login_required(login_url='/ingresar')
def acercaDe(request):
    return render_to_response('acercaDe.html')

@login_required(login_url='/ingresar')
def cerrarPeriodo(request):
    global user
    
    if user.has_perm('contable.add_estadoperiodo') == False:
        return render(request ,'error.html',{'mensaje':"No tiene permisos", 'link' : "/index"})
    global cerrar
    per = EstadoPeriodo()
    co=EstadoPeriodo.objects.all()
    for estado in co:
        if  estado.periodoActivo == True:
            per = estado
            per.periodoActivo = False
            per.cierre = True
    per.save()
    
    return render(request, 'error.html', {'mensaje' : "Se ha cerrado periodo contable", 'link' : "/index"})


#def registrarUsuario(request):
#    if request.method=='POST':
#        usuario=User()
#        group = user_group()
#        usuario.username = request.POST['nombre']
#        usuario.password = request.POST['pass']
#        usuario.email = request.POST['email']
#        usuario.is_active = '1'
#        group.
        
@login_required(login_url='/ingresar')
def costos(request):
    
    
    
    planilla=0.0
    sal=0.0
    c=Cuenta.objects.filter(id=3)
    p=Empleado.objects.all()
    for cu in c:
        sal=cu.saldo
    for emp in p:
        planilla=planilla+emp.salPagar
        
    f1=sal*0.6
    f2=sal*0.4
    s1=planilla*0.2
    s2=planilla*0.3
    s3=planilla*0.5
    t1=sal*0.1
    t2=sal*0.2
    t3=sal*0.7
    a1=30*0.75
    a2=30*0.25
    
    cuent=Cuenta.objects.all()

    sal2=0
    sal3=0
    sal4=0
    sal5=0
    for ct in cuent:
        if ct.id==10:
            sal2=ct.saldo
        elif ct.id==17:
            sal3=ct.saldo
        elif ct.id==16:
            sal4=ct.saldo
        elif ct.id==12:
            sal5=ct.saldo
    b1=(sal2/sal)*f1
    b2=(sal2/sal)*f2
    d1=(sal3/planilla)*s1
    d2=(sal3/planilla)*s2
    d3=(sal3/planilla)*s3
    e1=(sal4/sal)*t1
    e2=(sal4/sal)*t2
    e3=(sal4/sal)*t3
    g1=(sal5/30)*a1
    g2=(sal5/30)*a2
    
    m1=b1+d1+e1+g1
    m2=d2+e2
    m3=b2+d3+e3+g2
    
    m= m1+m3+m2 
    
    return render(request, 'costos.html',{'planilla':planilla,'cuenta':sal,'f1':f1,'f2':f2,'s1':s1,'s2':s2,'s3':s3,'t1':t1,'t2':t2,'t3':t3,'a1':a1,'a2':a2,'sal2':sal2,'sal3':sal3,'sal4':sal4,'sal5':sal5,'b1':b1,'b2':b2,'d1':d1,'d2':d2,'d3':d3,'e1':e1,'e2':e2,'e3':e3,'g1':g1,'g2':g2, 'm1':m1, 'm2':m2, 'm3':m3, 'm': m})
    
@login_required(login_url='/ingresar')
def peranteriores(request):
    
    p = EstadoPeriodo.objects.filter(periodoActivo = False  )
    if request.method == 'POST':
        per = request.POST['periodo']
        url = 'periodo/periodo'+ per +'.html'
        return  render(request,url,{})
    else:
        return render(request,'ElegirPeriodo.html', {'p':p})

@login_required(login_url='/ingresar')
def iniciarPeriodo(request):
    global cerrar
    
    co=EstadoPeriodo.objects.all()
    per = EstadoPeriodo()
    per.periodoContador=len(co)+1
    per.periodo = time.strftime("%x")
    per.cierre = False
    per.ajuste = False
    
    for estado in co:
        if  estado.periodoActivo == True:
            per.id=estado.id 
    per.save()
    cerrar = per
    return render(request, 'error.html', {'mensaje' : "Se ha inciado periodo contable", 'link' : "/index"})      
@login_required(login_url='/ingresar')
def ingresarUsuario(request):
    
    global user
    
    if user.has_perm('contable.add_empleado') == False:
        return render(request ,'error.html',{'mensaje':"No tiene permisos", 'link' : "/index"})
    
    if request.method == 'POST':
        if request.POST['contrasena'] == request.POST['contrasena2']:
            user = User.objects.create_user(username=request.POST['nombre'], email=request.POST['email'], password=request.POST['contrasena'])
            group = Group.objects.get(id = request.POST['permiso'])
            user.groups.add(group)
            user.save()
        else:
             return render(request, 'error.html', {'mensaje' : "Las contrase&ntilde;as no coinciden", 'link' : "/index"})
    return render(request, 'gest-usuario.html')