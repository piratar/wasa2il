# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-12-08 18:06
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('core', '0002_reset_migrations'),
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                (
                    'id',
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
                ('timestamp', models.DateTimeField(auto_now=True)),
                ('module', models.CharField(max_length=32)),
                ('action', models.CharField(max_length=32)),
                ('category', models.CharField(blank=True, max_length=64)),
                ('event', models.CharField(blank=True, max_length=1024)),
                (
                    'user',
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
    ]
