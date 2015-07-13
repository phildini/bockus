# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('readers', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='reader',
            name='name',
            field=models.CharField(null=True, max_length=100),
        ),
    ]
