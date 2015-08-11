# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import model_utils.fields
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('readers', '0001_initial'),
        ('books', '0002_auto_20150723_0552'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookEmail',
            fields=[
                ('id', models.AutoField(primary_key=True, verbose_name='ID', auto_created=True, serialize=False)),
                ('created', model_utils.fields.AutoCreatedField(editable=False, verbose_name='created', default=django.utils.timezone.now)),
                ('modified', model_utils.fields.AutoLastModifiedField(editable=False, verbose_name='modified', default=django.utils.timezone.now)),
                ('status', models.CharField(max_length='20', choices=[('pending', 'pending'), ('processing', 'processing'), ('sent', 'sent'), ('error', 'error')], default='pending')),
                ('book_file', models.ForeignKey(to='books.BookFileVersion')),
                ('reader', models.ForeignKey(to='readers.Reader')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AlterModelOptions(
            name='series',
            options={'verbose_name_plural': 'series'},
        ),
    ]
