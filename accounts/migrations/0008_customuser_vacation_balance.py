# Generated by Django 5.1.6 on 2025-03-07 12:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0007_remove_timetracking_vacation_balance'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='vacation_balance',
            field=models.IntegerField(default=30),
        ),
    ]
