# Generated by Django 5.1.2 on 2024-10-24 03:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vehicles', '0006_remove_payment_created_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='issue',
            name='component_action',
        ),
    ]
