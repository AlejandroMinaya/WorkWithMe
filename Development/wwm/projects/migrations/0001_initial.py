# Generated by Django 2.0.4 on 2018-04-12 19:17

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description', models.CharField(max_length=500)),
                ('progress', models.FloatField()),
                ('members', models.ManyToManyField(to='users.User')),
                ('projectOwner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='ProjectOwner', to='users.User')),
            ],
        ),
    ]
