# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0005_auto_20150817_2146'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bookonshelf',
            options={'verbose_name_plural': 'books on shelves'},
        ),
        migrations.AlterModelOptions(
            name='shelf',
            options={'verbose_name_plural': 'shelves'},
        ),
    ]
