# Generated by Django 3.2.4 on 2021-07-20 16:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('admin_books', '0004_auto_20210628_1523'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subscriber',
            fields=[
                ('id', models.PositiveIntegerField(primary_key=True, serialize=False, unique=True)),
            ],
        ),
    ]