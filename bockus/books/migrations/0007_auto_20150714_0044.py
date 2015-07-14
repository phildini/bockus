# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import model_utils.fields
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0006_remove_book_trove'),
    ]

    operations = [
        migrations.CreateModel(
            name='Series',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('created', model_utils.fields.AutoCreatedField(verbose_name='created', default=django.utils.timezone.now, editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(verbose_name='modified', default=django.utils.timezone.now, editable=False)),
                ('name', models.CharField(max_length=255)),
                ('author', models.CharField(null=True, max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='book',
            name='author',
            field=models.CharField(null=True, max_length=255),
        ),
        migrations.AddField(
            model_name='book',
            name='number_in_series',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='book',
            name='series',
            field=models.ForeignKey(to='books.Series', null=True),
        ),
    ]
