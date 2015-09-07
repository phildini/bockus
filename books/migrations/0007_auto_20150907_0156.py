# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0006_auto_20150821_2041'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookemail',
            name='reader',
            field=models.ForeignKey(on_delete=django.db.models.deletion.SET_NULL, to='readers.Reader', null=True, blank=True),
        ),
    ]
