# Generated by Django 3.1.7 on 2021-04-18 05:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='info_id',
            field=models.IntegerField(),
        ),
    ]
