# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('troves', '0003_auto_20150717_2306'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trove',
            name='meta',
            field=jsonfield.fields.JSONField(blank=True),
        ),
    ]
