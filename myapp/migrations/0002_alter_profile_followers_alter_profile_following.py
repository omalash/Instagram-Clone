# Generated by Django 4.2.2 on 2023-08-02 20:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='followers',
            field=models.ManyToManyField(related_name='followers_profiles', to='myapp.profile'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='following',
            field=models.ManyToManyField(related_name='following_profiles', to='myapp.profile'),
        ),
    ]
