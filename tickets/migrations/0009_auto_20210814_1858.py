# Generated by Django 3.1.13 on 2021-08-14 16:58

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('projects', '0017_auto_20210410_0750'),
        ('tickets', '0008_auto_20210613_0809'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='description',
            field=models.CharField(max_length=300),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='project',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='tickets', to='projects.project'),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='submitter',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='submitter_set', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='ticket',
            name='title',
            field=models.CharField(max_length=200, unique=True),
        ),
    ]
