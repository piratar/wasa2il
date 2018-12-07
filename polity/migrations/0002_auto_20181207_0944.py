# -*- coding: utf-8 -*-
# Generated by Django 1.11.16 on 2018-12-07 09:44
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('polity', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='polity',
            name='push_before_election_end',
            field=models.BooleanField(default=False, verbose_name='Send notification an hour before election ends?'),
        ),
        migrations.AddField(
            model_name='polity',
            name='push_before_vote_end',
            field=models.BooleanField(default=False, verbose_name='Send notification an hour before voting ends?'),
        ),
        migrations.AddField(
            model_name='polity',
            name='push_on_debate_start',
            field=models.BooleanField(default=False, verbose_name='Send notification when debate starts?'),
        ),
        migrations.AddField(
            model_name='polity',
            name='push_on_election_end',
            field=models.BooleanField(default=False, verbose_name='Send notification when an election ends?'),
        ),
        migrations.AddField(
            model_name='polity',
            name='push_on_election_start',
            field=models.BooleanField(default=False, verbose_name='Send notification when an election starts?'),
        ),
        migrations.AddField(
            model_name='polity',
            name='push_on_vote_end',
            field=models.BooleanField(default=False, verbose_name='Send notification when voting ends?'),
        ),
        migrations.AddField(
            model_name='polity',
            name='push_on_vote_start',
            field=models.BooleanField(default=False, verbose_name='Send notification when issue goes to vote?'),
        ),
    ]
