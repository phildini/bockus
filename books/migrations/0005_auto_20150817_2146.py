# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('libraries', '0003_libraryimport'),
        ('books', '0004_auto_20150811_0425'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookOnShelf',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('created', model_utils.fields.AutoCreatedField(verbose_name='created', default=django.utils.timezone.now, editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(verbose_name='modified', default=django.utils.timezone.now, editable=False)),
                ('book', models.ForeignKey(to='books.Book')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Shelf',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', serialize=False, auto_created=True)),
                ('created', model_utils.fields.AutoCreatedField(verbose_name='created', default=django.utils.timezone.now, editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(verbose_name='modified', default=django.utils.timezone.now, editable=False)),
                ('name', models.CharField(max_length=255)),
                ('meta', jsonfield.fields.JSONField(blank=True)),
                ('library', models.ForeignKey(to='libraries.Library')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='bookonshelf',
            name='shelf',
            field=models.ForeignKey(to='books.Shelf'),
        ),
    ]
