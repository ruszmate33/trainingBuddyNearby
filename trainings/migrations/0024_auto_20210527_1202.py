# Generated by Django 3.1 on 2021-05-27 10:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trainings', '0023_auto_20201020_0901'),
    ]

    operations = [
        migrations.AlterField(
            model_name='training',
            name='date',
            field=models.DateTimeField(default='2021-05-27 12:02'),
        ),
    ]
