# Generated by Django 2.2.25 on 2022-01-02 18:23

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('election', '0005_auto_20200909_1553'),
    ]

    operations = [
        migrations.AddField(
            model_name='election',
            name='conditions',
            field=models.TextField(blank=True, help_text='Candidates must accept these conditions to be allowed to run in the election. Anything binding for the candidates should be placed here, for example if candidates are expected to abide by certain rules, to volunteer their time in a some way or provide particular information.', null=True, verbose_name='Conditions for candidates'),
        ),
        migrations.AlterField(
            model_name='election',
            name='instructions',
            field=models.TextField(blank=True, help_text='Instructions or other information that might be of importance to those casting their votes.', null=True, verbose_name='Instructions for voters'),
        ),
        migrations.AlterUniqueTogether(
            name='candidate',
            unique_together={('user', 'election')},
        ),
    ]
