# -*- coding: utf-8 -*-
# Generated by Django 1.11.23 on 2019-08-29 18:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_userprofile_verified_assertion_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='phone',
            field=models.CharField(
                blank=True,
                help_text='Mostly intended for active participants such as volunteers and candidates.',
                max_length=30,
                null=True,
                verbose_name='Phone',
            ),
        ),
    ]
