# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0004_auto_20150703_2257'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bookfileversion',
            name='url',
        ),
        migrations.AddField(
            model_name='bookfileversion',
            name='path',
            field=models.CharField(null=True, max_length=255),
        ),
    ]
