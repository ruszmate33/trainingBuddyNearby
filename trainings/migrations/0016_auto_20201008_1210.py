# Generated by Django 3.1 on 2020-10-08 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trainings', '0015_auto_20201008_1152'),
    ]

    operations = [
        migrations.AlterField(
            model_name='training',
            name='date',
            field=models.DateTimeField(default='2020-10-08 12:10'),
        ),
    ]
