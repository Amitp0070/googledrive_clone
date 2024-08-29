from django.db import models
from django.contrib.auth.models import User
from PIL import Image
from django.core.files.base import ContentFile
from io import BytesIO

class Folder(models.Model):
    name = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='subfolders')
    created_at = models.DateTimeField(auto_now_add=True)
    is_trash = models.BooleanField(default=False)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

class File(models.Model):
    name = models.CharField(max_length=255)
    file = models.FileField(upload_to='files/')
    thumbnail = models.ImageField(upload_to='thumbnails/', blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE, null=True, blank=True, related_name='files')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, related_name='children')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_spam = models.BooleanField(default=False)
    is_trash = models.BooleanField(default=False)
    url = models.URLField(default='http://127.0.0.1.8000')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        self.generate_thumbnail()

    def generate_thumbnail(self):
        if self.file and not self.thumbnail:
            if self.file.name.lower().endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp')):
                img = Image.open(self.file.path)
                img.thumbnail((200, 200))
                thumb_io = BytesIO()
                img.save(thumb_io, format='PNG')
                thumbnail = ContentFile(thumb_io.getvalue())
                self.thumbnail.save(f"{self.name}_thumb.png", thumbnail, save=False)
                self.save()

class SharedFile(models.Model):
    file = models.ForeignKey(File, on_delete=models.CASCADE, related_name='shared_with')
    shared_with = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shared_files')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('file', 'shared_with')

class SharedFolder(models.Model):
    folder = models.ForeignKey(Folder, on_delete=models.CASCADE, related_name='shared_with')
    shared_with = models.ForeignKey(User, on_delete=models.CASCADE, related_name='shared_folders')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('folder', 'shared_with')