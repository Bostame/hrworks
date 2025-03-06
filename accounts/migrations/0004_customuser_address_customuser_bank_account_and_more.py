# Generated by Django 5.1.6 on 2025-03-06 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_alter_customuser_profile_picture'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='address',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='bank_account',
            field=models.CharField(blank=True, max_length=34, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='child_birthdate',
            field=models.DateField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='child_name',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='customuser',
            name='health_insurance',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
