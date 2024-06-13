# Generated by Django 4.0.4 on 2022-10-04 11:07

import authentication.models
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='CustomUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.TextField(blank=True, max_length=30, null=True, verbose_name='first_name')),
                ('last_name', models.TextField(blank=True, max_length=30, null=True, verbose_name='last_name')),
                ('email', models.EmailField(max_length=200, unique=True, verbose_name='email address')),
                ('password', models.TextField(blank=True, max_length=150, null=True, verbose_name='password')),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='users/avatars')),
                ('about', models.TextField(blank=True, default='', max_length=200, null=True)),
                ('cover', models.ImageField(blank=True, null=True, upload_to='users/covers')),
                ('date_joined', models.DateTimeField(auto_now_add=True, null=True, verbose_name='date_joined')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last_login')),
                ('is_subscribed', models.BooleanField(blank=True, default=False, verbose_name='is_subscribed')),
                ('is_active', models.BooleanField(blank=True, default=False, null=True)),
                ('is_superuser', models.BooleanField(blank=True, default=False, null=True)),
                ('is_admin', models.BooleanField(blank=True, default=False, null=True)),
                ('is_staff', models.BooleanField(blank=True, default=False, null=True)),
                ('is_employee', models.BooleanField(blank=True, default=False, null=True)),
            ],
            options={
                'abstract': False,
            },
            managers=[
                ('objects', authentication.models.CustomUserManager()),
            ],
        ),
    ]
