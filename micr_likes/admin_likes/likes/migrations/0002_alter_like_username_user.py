# Generated by Django 3.2.5 on 2021-07-06 15:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('likes', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='like',
            name='username_user',
            field=models.CharField(max_length=255),
        ),
    ]
