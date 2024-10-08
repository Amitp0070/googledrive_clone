# Generated by Django 5.1 on 2024-08-26 16:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('drive', '0005_driveitem_delete_item'),
    ]

    operations = [
        migrations.AddField(
            model_name='file',
            name='thumbnail',
            field=models.ImageField(blank=True, null=True, upload_to='thumbnails/files/'),
        ),
        migrations.AddField(
            model_name='folder',
            name='thumbnail',
            field=models.ImageField(blank=True, null=True, upload_to='thumbnails/folders/'),
        ),
        migrations.DeleteModel(
            name='DriveItem',
        ),
    ]
