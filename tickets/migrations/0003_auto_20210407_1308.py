# Generated by Django 3.1.7 on 2021-04-07 13:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0002_auto_20210407_1257'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='description',
            field=models.CharField(max_length=301),
        ),
    ]