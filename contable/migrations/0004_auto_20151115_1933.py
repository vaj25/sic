# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contable', '0003_estadoscuentas_cierre'),
    ]

    operations = [
        migrations.AlterField(
            model_name='estadoscuentas',
            name='cierre',
            field=models.BooleanField(default=b'False'),
        ),
    ]
