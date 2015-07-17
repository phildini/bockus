# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('troves', '0003_auto_20150717_2306'),
        ('books', '0008_auto_20150717_0350'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='trove',
            field=models.ForeignKey(null=True, to='troves.Trove'),
        ),
        migrations.AddField(
            model_name='series',
            name='trove',
            field=models.ForeignKey(null=True, to='troves.Trove'),
        ),
    ]
