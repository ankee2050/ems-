# Generated by Django 2.0 on 2020-04-05 12:02

import django.contrib.auth.models
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
        ('employee', '0003_profile_picture'),
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
            ],
            options={
                'ordering': ('last_name',),
                'proxy': True,
                'indexes': [],
            },
            bases=('auth.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.AlterField(
            model_name='profile',
            name='picture',
            field=models.ImageField(blank=True, max_length=255, null=True, upload_to='profile_pictures/%Y/%m/%d/'),
        ),
    ]
