# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        ('libraries', '0003_libraryimport'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Invitation',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True, serialize=False)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('changed', models.DateTimeField(auto_now=True)),
                ('status', models.CharField(choices=[('pending', 'pending'), ('processing', 'processing'), ('error', 'error'), ('sent', 'sent'), ('accepted', 'accepted')], max_length=100, default='pending')),
                ('email', models.EmailField(max_length=254)),
                ('sent', models.DateTimeField(null=True)),
                ('key', models.CharField(unique=True, max_length=32)),
                ('library', models.ForeignKey(blank=True, to='libraries.Library', null=True)),
                ('sender', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
