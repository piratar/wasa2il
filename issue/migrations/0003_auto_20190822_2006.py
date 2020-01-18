# Generated by Django 2.2.4 on 2019-08-22 20:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('issue', '0002_auto_20181124_1740'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='created_by',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='comment_created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='comment',
            name='modified_by',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='comment_modified_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='document',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='documentcontent',
            name='predecessor',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='issue.DocumentContent'),
        ),
        migrations.AlterField(
            model_name='documentcontent',
            name='status',
            field=models.CharField(choices=[('proposed', 'Proposed'), ('accepted', 'Accepted'), ('rejected', 'Rejected'), ('deprecated', 'Deprecated'), ('retracted', 'Retracted')], default='proposed', max_length=32),
        ),
        migrations.AlterField(
            model_name='documentcontent',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='issue',
            name='created_by',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='issue_created_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='issue',
            name='documentcontent',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='issue', to='issue.DocumentContent'),
        ),
        migrations.AlterField(
            model_name='issue',
            name='modified_by',
            field=models.ForeignKey(blank=True, editable=False, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='issue_modified_by', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='issue',
            name='ruleset',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='polity.PolityRuleset', verbose_name='Ruleset'),
        ),
        migrations.AlterField(
            model_name='issue',
            name='special_process',
            field=models.CharField(blank=True, choices=[('accepted_at_assembly', 'Accepted at assembly'), ('rejected_at_assembly', 'Rejected at assembly'), ('retracted', 'Retracted')], default='', max_length=32, null=True, verbose_name='Special process'),
        ),
        migrations.AlterField(
            model_name='issue',
            name='special_process_set_by',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='special_process_issues', to=settings.AUTH_USER_MODEL),
        ),
    ]
