# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contable', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EstadosCuentas',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('periodo', models.DateField()),
                ('cuenta', models.ForeignKey(to='contable.Cuenta')),
                ('tipoMonto', models.ForeignKey(to='contable.TipoMonto')),
            ],
        ),
        migrations.DeleteModel(
            name='Usuario',
        ),
    ]
