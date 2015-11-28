# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Cuenta',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nom_cuenta', models.CharField(max_length=30)),
                ('saldo', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Empleado',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nombre', models.CharField(max_length=30)),
                ('apellido', models.CharField(max_length=30)),
                ('salAgregado', models.FloatField()),
                ('horas', models.IntegerField()),
                ('horasExtras', models.IntegerField()),
                ('dui', models.CharField(max_length=10)),
                ('nit', models.CharField(max_length=17)),
            ],
        ),
        migrations.CreateModel(
            name='Puesto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nom_puesto', models.CharField(max_length=30)),
                ('salBase', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='TipoCuenta',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nom_Tipocuenta', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='TipoMonto',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('nom_tipoMonto', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Transaccion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('monto', models.FloatField()),
                ('fecha', models.DateField()),
                ('cuenta', models.ForeignKey(to='contable.Cuenta')),
                ('tipoMonto', models.ForeignKey(to='contable.TipoMonto')),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('codigo', models.CharField(max_length=8)),
                ('password', models.CharField(max_length=15)),
                ('nombre', models.CharField(max_length=30)),
            ],
        ),
        migrations.AddField(
            model_name='empleado',
            name='puesto',
            field=models.ForeignKey(to='contable.Puesto'),
        ),
        migrations.AddField(
            model_name='cuenta',
            name='tipoCuenta',
            field=models.ForeignKey(to='contable.TipoCuenta'),
        ),
    ]
