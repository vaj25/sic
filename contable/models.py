from django.db import models

class Puesto(models.Model):
    nom_puesto = models.CharField(max_length=30)
    salBase = models.FloatField()
    pHoraExtra= models.FloatField()
    
class Empleado(models.Model):
    nombre = models.CharField(max_length=30)
    apellido = models.CharField(max_length=30)
    horasExtras = models.IntegerField()
    dui = models.CharField(max_length=10)
    nit = models.CharField(max_length=17)
    isss = models.FloatField()
    afp = models.FloatField()
    renta = models.FloatField()
    salDevengado = models.FloatField()
    salPagar = models.FloatField()
    puesto = models.ForeignKey(Puesto)
    
    
class TipoCuenta(models.Model):
    nom_Tipocuenta = models.CharField(max_length=30)
    
class TipoMonto (models.Model):
    nom_tipoMonto = models.CharField(max_length=30)
    
class Cuenta(models.Model):
    nom_cuenta = models.CharField(max_length=30)
    saldo = models.FloatField()
    tipoCuenta = models.ForeignKey(TipoCuenta)
    montoCargo=models.FloatField()
    montoAbono=models.FloatField()
    
class Transaccion(models.Model):    
    monto =  models.FloatField()
    fecha = models.CharField(max_length=20)
    cuenta = models.ForeignKey(Cuenta)
    tipoMonto =  models.ForeignKey(TipoMonto)
        
class EstadoPeriodo(models.Model):
    periodo = models.CharField(max_length=20)
    cierre = models.BooleanField(default='False')
    
    
class Transacciones(models.Model):
    cuenta = models.ForeignKey(Cuenta)
    numero=models.IntegerField()
    cargo=models.FloatField()
    abono=models.FloatField()
    fecha=models.CharField(max_length=20)
    
class comprobacion(models.Model):
    estadoPeriodo = models.ForeignKey(EstadoPeriodo)
    nombreCuenta=models.CharField(max_length=30)
    debe=models.FloatField()
    haber=models.FloatField()
    
    
    

    