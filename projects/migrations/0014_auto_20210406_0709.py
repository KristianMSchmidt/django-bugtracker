# Generated by Django 3.1.7 on 2021-04-06 07:09

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projects', '0013_auto_20210406_0635'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='users',
            field=models.ManyToManyField(related_name='xprojects', to=settings.AUTH_USER_MODEL),
        ),
    ]
