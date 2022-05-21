# Generated by Django 3.1.5 on 2021-01-16 20:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0007_merge_20191019_1939'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='email_wanted',
            field=models.BooleanField(
                default=False,
                help_text='Whether to consent to receiving notifications via email.',
                null=True,
                verbose_name='Consent for sending email',
            ),
        ),
    ]
