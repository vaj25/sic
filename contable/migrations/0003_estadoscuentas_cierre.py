# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contable', '0002_auto_20151115_1911'),
    ]

    operations = [
        migrations.AddField(
            model_name='estadoscuentas',
            name='cierre',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
    ]
