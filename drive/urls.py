from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('my-drive/', views.my_drive, name='my_drive'),
    path('shared-with-me/', views.shared_with_me, name='shared_with_me'),
    path('recent/', views.recent, name='recent'),
    path('starred/', views.starred, name='starred'),
    path('spam/', views.spam, name='spam'),
    path('storage/', views.storage, name='storage'),
    path('upload/', views.upload_file, name='upload_file'),
    path('create-folder/', views.create_folder, name='create_folder'),
    path('folder/<int:id>/', views.folder_detail, name='folder_detail'),
    path('share-file/<int:file_id>/', views.share_file, name='share_file'),
    path('share-folder/<int:folder_id>/', views.share_folder, name='share_folder'),
    path('search/', views.search, name='search'),
    
    # Trash and deletion related URLs
    path('trash/', views.trash_list, name='trash_list'),
    path('restore_file/<int:file_id>/', views.restore_file, name='restore_file'),
    path('restore_folder/<int:folder_id>/', views.restore_folder, name='restore_folder'),
    path('delete_file_permanently/<int:file_id>/', views.delete_file_permanently, name='delete_file_permanently'),
    path('delete_folder_permanently/<int:folder_id>/', views.delete_folder_permanently, name='delete_folder_permanently'),
    path('move_to_trash_file/<int:file_id>/', views.move_to_trash_file, name='move_to_trash_file'),
    path('move_to_trash_folder/<int:folder_id>/', views.move_to_trash_folder, name='move_to_trash_folder'),
]
