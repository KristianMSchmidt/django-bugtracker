# Generated by Django 3.1.7 on 2021-04-08 10:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0003_auto_20210407_1308'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='priority',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Low'), (2, 'Medium'), (3, 'High'), (4, 'Urgent')], null=True),
        ),
    ]