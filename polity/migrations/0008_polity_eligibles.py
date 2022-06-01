# Generated by Django 2.2.17 on 2021-01-16 20:10

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('polity', '0007_polity_name_short'),
    ]

    operations = [
        migrations.AddField(
            model_name='polity',
            name='eligibles',
            field=models.ManyToManyField(
                related_name='polities_eligible', to=settings.AUTH_USER_MODEL
            ),
        ),
    ]
