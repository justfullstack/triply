# Generated by Django 4.0.4 on 2022-10-16 12:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0006_remove_customuser_profile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='customuser',
            name='avatar',
            field=models.ImageField(blank=True, default='defaults/avatar.jpg', null=True, upload_to='users/avatars'),
        ),
        migrations.AlterField(
            model_name='customuser',
            name='cover',
            field=models.ImageField(blank=True, default='defaults/cover.jpg', null=True, upload_to='users/covers'),
        ),
    ]