# Generated by Django 3.1.7 on 2021-04-15 08:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tickets', '0002_ticketevent'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ticketevent',
            name='new_value',
        ),
        migrations.RemoveField(
            model_name='ticketevent',
            name='old_value',
        ),
        migrations.AlterField(
            model_name='ticketevent',
            name='property_changed',
            field=models.IntegerField(choices=[(1, 'Status Change'), (2, 'Priority Change'), (3, 'Type Change'), (4, 'Developer Change'), (5, 'Title Change'), (6, 'Description Change'), (7, 'Deleted Change')]),
        ),
    ]