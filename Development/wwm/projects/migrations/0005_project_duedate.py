# Generated by Django 2.0.4 on 2018-04-18 22:23

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('projects', '0004_remove_project_description'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='dueDate',
            field=models.DateField(default=datetime.date(199, 1, 21)),
        ),
    ]