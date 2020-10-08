# Generated by Django 3.1 on 2020-10-08 09:52

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('trainings', '0014_auto_20201008_0932'),
    ]

    operations = [
        migrations.AlterField(
            model_name='training',
            name='date',
            field=models.DateTimeField(default='2020-10-08 11:52'),
        ),
        migrations.CreateModel(
            name='Athlete',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('trainings', models.ManyToManyField(blank=True, related_name='participants', to='trainings.Training')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
