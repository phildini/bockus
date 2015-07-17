# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0009_auto_20150717_2306'),
    ]

    operations = [
        migrations.AddField(
            model_name='series',
            name='meta',
            field=jsonfield.fields.JSONField(blank=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='meta',
            field=jsonfield.fields.JSONField(blank=True),
        ),
    ]
