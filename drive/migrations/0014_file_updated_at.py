# Generated by Django 5.1 on 2024-08-27 06:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drive', '0013_file_is_trash'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
