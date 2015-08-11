# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0003_auto_20150811_0403'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookemail',
            name='status',
            field=models.CharField(choices=[('pending', 'pending'), ('processing', 'processing'), ('sent', 'sent'), ('error', 'error')], default='pending', max_length=20),
        ),
    ]
