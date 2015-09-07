# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('readers', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='reader',
            name='kind',
            field=models.CharField(max_length=10, choices=[('iBooks', 'iBooks (.epub, .pdf)'), ('Kindle', 'Kindle (.mobi, .pdf)')]),
        ),
    ]
