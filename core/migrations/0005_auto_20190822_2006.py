# Generated by Django 2.2.4 on 2019-08-22 20:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_userprofile_declaration_of_interests'),
    ]

    operations = [
        migrations.AlterField(
            model_name='event',
            name='user',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='language',
            field=models.CharField(
                choices=[('is', 'Íslenska'), ('en', 'English')],
                default='en',
                max_length=6,
                verbose_name='Language',
            ),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='picture',
            field=models.ImageField(
                blank=True,
                null=True,
                upload_to='profiles',
                verbose_name='Picture',
            ),
        ),
    ]
