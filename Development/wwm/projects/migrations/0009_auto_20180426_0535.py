# Generated by Django 2.0.4 on 2018-04-26 05:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_auto_20180418_2204'),
        ('projects', '0008_recentactivy'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='RecentActivy',
            new_name='RecentActivity',
        ),
    ]
