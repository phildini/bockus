# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0007_auto_20150714_0044'),
    ]

    operations = [
        migrations.AlterField(
            model_name='book',
            name='author',
            field=models.CharField(null=True, blank=True, max_length=255),
        ),
        migrations.AlterField(
            model_name='book',
            name='number_in_series',
            field=models.IntegerField(null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='book',
            name='series',
            field=models.ForeignKey(null=True, to='books.Series', blank=True),
        ),
        migrations.AlterField(
            model_name='series',
            name='author',
            field=models.CharField(null=True, blank=True, max_length=255),
        ),
    ]
