# Generated by Django 3.1.7 on 2021-04-05 10:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('projects', '0012_delete_ticket'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Ticket',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.CharField(default='', max_length=301)),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('updated_at', models.DateTimeField(auto_now=True, null=True)),
                ('status', models.CharField(choices=[('OP', 'Open'), ('IP', 'In progress'), ('CL', 'Closed'), ('IR', 'More info required')], default='OP', max_length=2)),
                ('priority', models.CharField(choices=[('L', 'Low'), ('M', 'Medium'), ('H', 'High'), ('U', 'Urgent')], default='L', max_length=1)),
                ('type', models.CharField(choices=[('FR', 'Feature request'), ('BG', 'Bug/Error'), ('OT', 'Other')], default='OP', max_length=2)),
                ('developer', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='developer', to=settings.AUTH_USER_MODEL)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='tickets', to='projects.project')),
                ('submitter', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='submitter', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
