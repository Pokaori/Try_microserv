# Generated by Django 3.2.4 on 2021-06-28 15:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_books', '0003_auto_20210625_1813'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='books',
            name='id_publisher',
        ),
        migrations.AddField(
            model_name='books',
            name='username_publisher',
            field=models.CharField(default=11, max_length=255),
            preserve_default=False,
        ),
    ]
