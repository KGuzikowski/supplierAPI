# Generated by Django 3.1.3 on 2020-12-09 09:43

from django.db import migrations

from supplierapi.apps.general.serializers import IndustrySerializer


def insert_industries(apps, schema_editor):
    Industry = apps.get_model('general', 'Industry')
    with open('../industries.txt') as file:
        for line in file:
            data = line.split('|')
            for i, name in enumerate(data):
                parent: str
                serializer = IndustrySerializer(data={'name': name})
                if serializer.is_valid(raise_exception=True):
                    if i == 0:
                        new_industry = Industry(name=serializer.validated_data['name'])
                        new_industry.save()
                        parent = name
                    else:
                        parent_industry = Industry.objects.get(name=parent)
                        new_industry = Industry(
                            name=serializer.validated_data['name'],
                            parent_industry=parent_industry,
                        )
                        new_industry.save()


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(insert_industries)
    ]
