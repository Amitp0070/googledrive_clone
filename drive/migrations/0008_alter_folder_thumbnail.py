# Generated by Django 5.1 on 2024-08-26 16:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drive', '0007_alter_file_thumbnail'),
    ]

    operations = [
        migrations.AlterField(
            model_name='folder',
            name='thumbnail',
            field=models.ImageField(blank=True, null=True, upload_to='thumbnails/'),
        ),
    ]
