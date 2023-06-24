# Generated by Django 4.2.2 on 2023-06-24 15:11

from django.db import migrations, models
import myapp.models


class Migration(migrations.Migration):

    dependencies = [
        ('myapp', '0003_userprofile_pfp_alter_post_caption_alter_post_image_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='description',
            field=models.CharField(default='', max_length=150, null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='pfp',
            field=models.ImageField(default='default_pfp.jpg', null=True, upload_to=myapp.models.user_profile_picture_path),
        ),
    ]
