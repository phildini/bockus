# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import jsonfield.fields


class Migration(migrations.Migration):

    dependencies = [
        ('books', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='BookFileVersion',
            fields=[
                ('id', models.AutoField(serialize=False, verbose_name='ID', primary_key=True, auto_created=True)),
                ('filetype', models.CharField(max_length=10, choices=[('ePub', 'epub'), ('PDF', 'pdf'), ('Mobi', 'mobi')])),
                ('url', models.URLField()),
                ('meta', jsonfield.fields.JSONField()),
            ],
        ),
        migrations.RemoveField(
            model_name='book',
            name='url',
        ),
        migrations.AddField(
            model_name='bookfileversion',
            name='book',
            field=models.ForeignKey(to='books.Book'),
        ),
    ]
