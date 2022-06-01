# Generated by Django 3.1.5 on 2021-01-18 23:42

from django.db import migrations

# When polity types were first introduced, they were enumerated with a
# single-letter with the default "U" for "unspecified" and so forth. We are
# changing to more descriptive strings which are expected to exist and so we
# must update previous data.
def update_polity_types(apps, schema_editor):
    Polity = apps.get_model('polity', 'Polity')
    Polity.objects.filter(polity_type='U').update(polity_type='unspecified')
    Polity.objects.filter(polity_type='R').update(polity_type='regional')
    Polity.objects.filter(polity_type='C').update(polity_type='constituency')
    Polity.objects.filter(polity_type='I').update(
        polity_type='special_interest'
    )


class Migration(migrations.Migration):

    dependencies = [
        ('polity', '0011_auto_20210118_2303'),
    ]

    operations = [migrations.RunPython(update_polity_types)]
