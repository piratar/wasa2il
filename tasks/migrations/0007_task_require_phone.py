# -*- coding: utf-8 -*-
# Generated by Django 1.11.23 on 2019-09-01 14:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0006_auto_20190831_1804'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='require_phone',
            field=models.BooleanField(default=True, help_text='Make users provide their phone numbers in the profiles to partake in the task.', verbose_name='Require phone number from volunteers'),
        ),
    ]
