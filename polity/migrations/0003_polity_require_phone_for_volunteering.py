# -*- coding: utf-8 -*-
# Generated by Django 1.11.23 on 2019-09-01 12:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polity', '0002_auto_20181207_0944'),
    ]

    operations = [
        migrations.AddField(
            model_name='polity',
            name='require_phone_for_volunteering',
            field=models.BooleanField(
                default=True,
                help_text='Make users provide their phone numbers in the profiles to partake in tasks that need volunteers.',
                verbose_name='Require phone for volunteering',
            ),
        ),
    ]
