from django.contrib import admin
from .models import Folder, File, SharedFile, SharedFolder

class FolderAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'parent', 'created_at')
    list_filter = ('owner', 'created_at')
    search_fields = ('name', 'owner__username')

class FileAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'folder', 'uploaded_at')
    list_filter = ('owner', 'uploaded_at')
    search_fields = ('name', 'owner__username')
    readonly_fields = ('thumbnail',)

    def thumbnail_tag(self, obj):
        if obj.thumbnail:
            return mark_safe(f'<img src="{obj.thumbnail.url}" width="50" height="50" />')
        return "-"
    thumbnail_tag.short_description = 'Thumbnail'

class SharedFileAdmin(admin.ModelAdmin):
    list_display = ('file', 'shared_with', 'created_at')
    list_filter = ('shared_with', 'created_at')
    search_fields = ('file__name', 'shared_with__username')

class SharedFolderAdmin(admin.ModelAdmin):
    list_display = ('folder', 'shared_with', 'created_at')
    list_filter = ('shared_with', 'created_at')
    search_fields = ('folder__name', 'shared_with__username')

admin.site.register(Folder, FolderAdmin)
admin.site.register(File, FileAdmin)
admin.site.register(SharedFile, SharedFileAdmin)
admin.site.register(SharedFolder, SharedFolderAdmin)
