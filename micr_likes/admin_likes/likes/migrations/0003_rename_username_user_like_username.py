# Generated by Django 3.2.5 on 2021-07-06 15:45

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('likes', '0002_alter_like_username_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='like',
            old_name='username_user',
            new_name='username',
        ),
    ]
