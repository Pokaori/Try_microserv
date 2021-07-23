# Generated by Django 3.2.5 on 2021-07-09 17:11

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('likes', '0003_rename_username_user_like_username'),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.PositiveIntegerField(primary_key=True, serialize=False, unique=True)),
            ],
        ),
        migrations.AlterField(
            model_name='like',
            name='id_book',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='likes.book'),
        ),
    ]