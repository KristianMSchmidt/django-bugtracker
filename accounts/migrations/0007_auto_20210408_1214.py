# Generated by Django 3.1.7 on 2021-04-08 10:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_auto_20210408_1209'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='role',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Developer'), (2, 'Admin'), (3, 'Project Manager')], default=1, null=True),
        ),
    ]
