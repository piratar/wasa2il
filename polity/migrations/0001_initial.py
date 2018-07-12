# -*- coding: utf-8 -*-
# Generated by Django 1.11.13 on 2018-07-12 14:16
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Polity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=128, verbose_name='Name')),
                ('slug', models.SlugField(blank=True, max_length=128)),
                ('description', models.TextField(blank=True, null=True, verbose_name='Description')),
                ('is_listed', models.BooleanField(default=True, help_text='Whether the polity is publicly listed or not.', verbose_name='Publicly listed?')),
                ('is_newissue_only_officers', models.BooleanField(default=False, help_text="If this is checked, only officers can create new issues. If it's unchecked, any member can start a new issue.", verbose_name='Can only officers make new issues?')),
                ('is_front_polity', models.BooleanField(default=False, help_text='If checked, this polity will be displayed on the front page. The first created polity automatically becomes the front polity.', verbose_name='Front polity?')),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('modified', models.DateTimeField(auto_now=True)),
                ('created_by', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polity_created_by', to=settings.AUTH_USER_MODEL)),
                ('members', models.ManyToManyField(related_name='polities', to=settings.AUTH_USER_MODEL)),
                ('modified_by', models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polity_modified_by', to=settings.AUTH_USER_MODEL)),
                ('officers', models.ManyToManyField(related_name='officers', to=settings.AUTH_USER_MODEL, verbose_name='Officers')),
                ('parent', models.ForeignKey(blank=True, help_text=b'Parent polity', null=True, on_delete=django.db.models.deletion.CASCADE, to='polity.Polity')),
                ('wranglers', models.ManyToManyField(related_name='wranglers', to=settings.AUTH_USER_MODEL, verbose_name='Volunteer wranglers')),
            ],
        ),
        migrations.CreateModel(
            name='PolityRuleset',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('issue_majority', models.DecimalField(decimal_places=2, max_digits=5)),
                ('issue_discussion_time', models.DurationField()),
                ('issue_proposal_time', models.DurationField()),
                ('issue_vote_time', models.DurationField()),
                ('polity', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='polity.Polity')),
            ],
        ),
    ]
