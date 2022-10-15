# Generated by Django 4.0.4 on 2022-10-12 08:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0003_remove_profile_city_remove_profile_country_and_more'),
        ('authentication', '0004_alter_customuser_options_customuser_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='customuser',
            name='profile',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='profile', to='profiles.profile'),
            preserve_default=False,
        ),
    ]
