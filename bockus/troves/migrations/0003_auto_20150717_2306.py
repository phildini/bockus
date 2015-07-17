# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.utils.timezone
import model_utils.fields
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('troves', '0002_auto_20150703_2257'),
    ]

    operations = [
        migrations.CreateModel(
            name='TroveLibrarian',
            fields=[
                ('id', models.AutoField(auto_created=True, verbose_name='ID', serialize=False, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='trove',
            name='allowed_users',
            field=models.IntegerField(default=5),
        ),
        migrations.AddField(
            model_name='trovelibrarian',
            name='trove',
            field=models.ForeignKey(to='troves.Trove'),
        ),
        migrations.AddField(
            model_name='trovelibrarian',
            name='user',
            field=models.ForeignKey(to=settings.AUTH_USER_MODEL),
        ),
    ]
