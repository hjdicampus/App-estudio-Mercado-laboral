# Generated by Django 5.2 on 2025-04-10 08:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('job_market', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='joboffer',
            name='location',
            field=models.CharField(blank=True, max_length=200, null=True),
        ),
        migrations.AlterField(
            model_name='joboffer',
            name='salary',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
