# Generated by Django 3.1.7 on 2021-04-08 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20210405_1800'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='role',
            field=models.CharField(choices=[(1, 'Developer'), (2, 'Admin'), (3, 'Project Manager')], default=1, max_length=2),
        ),
    ]