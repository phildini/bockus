# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import model_utils.fields


class Migration(migrations.Migration):

    dependencies = [
        ('libraries', '0002_auto_20150811_0403'),
    ]

    operations = [
        migrations.CreateModel(
            name='LibraryImport',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False, verbose_name='ID', auto_created=True)),
                ('created', model_utils.fields.AutoCreatedField(editable=False, default=django.utils.timezone.now, verbose_name='created')),
                ('modified', model_utils.fields.AutoLastModifiedField(editable=False, default=django.utils.timezone.now, verbose_name='modified')),
                ('source', models.CharField(max_length=20, choices=[('dropbox', 'dropbox')], default='dropbox')),
                ('status', models.CharField(max_length=20, choices=[('pending', 'pending'), ('processing', 'processing'), ('done', 'done'), ('error', 'error')], default='pending')),
                ('path', models.TextField()),
                ('librarian', models.ForeignKey(to='libraries.Librarian')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
