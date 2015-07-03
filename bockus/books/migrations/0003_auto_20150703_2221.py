# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0002_auto_20150703_1910'),
    ]

    operations = [
        migrations.AddField(
            model_name='bookfileversion',
            name='storage_provider',
            field=models.CharField(default='dropbox', max_length=10, choices=[('dropbox', 'dropbox')]),
        ),
        migrations.AlterField(
            model_name='bookfileversion',
            name='filetype',
            field=models.CharField(choices=[('epub', 'epub'), ('pdf', 'pdf'), ('mobi', 'mobi')], max_length=10),
        ),
    ]
