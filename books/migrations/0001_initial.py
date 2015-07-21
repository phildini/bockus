# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields
import model_utils.fields
import django.utils.timezone
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('libraries', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('created', model_utils.fields.AutoCreatedField(verbose_name='created', default=django.utils.timezone.now, editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(verbose_name='modified', default=django.utils.timezone.now, editable=False)),
                ('title', models.CharField(max_length=255)),
                ('author', models.CharField(null=True, blank=True, max_length=255)),
                ('number_in_series', models.IntegerField(null=True, blank=True)),
                ('meta', jsonfield.fields.JSONField(blank=True)),
                ('added_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
                ('library', models.ForeignKey(to='libraries.Library')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='BookFileVersion',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('created', model_utils.fields.AutoCreatedField(verbose_name='created', default=django.utils.timezone.now, editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(verbose_name='modified', default=django.utils.timezone.now, editable=False)),
                ('filetype', models.CharField(choices=[('epub', 'epub'), ('pdf', 'pdf'), ('mobi', 'mobi')], max_length=10)),
                ('storage_provider', models.CharField(default='dropbox', choices=[('dropbox', 'dropbox')], max_length=10)),
                ('path', models.CharField(null=True, max_length=255)),
                ('meta', jsonfield.fields.JSONField()),
                ('book', models.ForeignKey(to='books.Book')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Series',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('created', model_utils.fields.AutoCreatedField(verbose_name='created', default=django.utils.timezone.now, editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(verbose_name='modified', default=django.utils.timezone.now, editable=False)),
                ('name', models.CharField(max_length=255)),
                ('author', models.CharField(null=True, blank=True, max_length=255)),
                ('meta', jsonfield.fields.JSONField(blank=True)),
                ('library', models.ForeignKey(to='libraries.Library')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='book',
            name='series',
            field=models.ForeignKey(null=True, to='books.Series', blank=True),
        ),
    ]
