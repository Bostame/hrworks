# Generated by Django 5.1.6 on 2025-03-08 14:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0011_customuser_role'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='customuser',
            name='role',
        ),
    ]
