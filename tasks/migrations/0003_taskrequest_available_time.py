# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2019-07-30 23:50
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_auto_20190730_2053'),
    ]

    operations = [
        migrations.AddField(
            model_name='taskrequest',
            name='available_time',
            field=models.TextField(
                default='', verbose_name='What available time do I have?'
            ),
            preserve_default=False,
        ),
    ]
