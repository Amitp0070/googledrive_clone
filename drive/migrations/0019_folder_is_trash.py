# Generated by Django 5.1 on 2024-08-27 10:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drive', '0018_file_updated_at'),
    ]

    operations = [
        migrations.AddField(
            model_name='folder',
            name='is_trash',
            field=models.BooleanField(default=False),
        ),
    ]
