# Generated by Django 5.1.2 on 2024-10-23 15:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vehicles', '0003_rename_owner_vehicle_company_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='issue',
            old_name='component',
            new_name='components',
        ),
    ]
