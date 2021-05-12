# Generated by Django 3.0.6 on 2020-11-15 17:24

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('company', '0001_initial'),
        ('general', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='company',
            name='country_of_registration',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='general.Country'),
        ),
        migrations.AddField(
            model_name='company',
            name='industry',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='general.Industry'),
        ),
        migrations.AddField(
            model_name='company',
            name='owners',
            field=models.ManyToManyField(to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='address',
            name='company',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='localizations', to='company.Company'),
        ),
        migrations.AddField(
            model_name='address',
            name='country',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='general.Country'),
        ),
        migrations.AddConstraint(
            model_name='role',
            constraint=models.UniqueConstraint(fields=('company', 'name'), name='company_role_unique_together'),
        ),
        migrations.AddConstraint(
            model_name='phonenumber',
            constraint=models.UniqueConstraint(fields=('dialing_code', 'number'), name='company_phonenumber_unique_together'),
        ),
        migrations.AddConstraint(
            model_name='employee',
            constraint=models.UniqueConstraint(fields=('company', 'user'), name='company_employee_unique_together'),
        ),
    ]