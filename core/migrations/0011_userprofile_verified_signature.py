# Generated by Django 5.1 on 2024-08-30 10:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_auto_20231130_1855'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='verified_signature',
            field=models.CharField(blank=True, max_length=4096, null=True),
        ),
    ]
