# Generated by Django 3.1.7 on 2021-04-05 07:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0006_ticket'),
    ]

    operations = [
        migrations.AddField(
            model_name='ticket',
            name='description',
            field=models.CharField(default='', max_length=301),
        ),
    ]
