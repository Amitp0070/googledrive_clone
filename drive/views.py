from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import File, Folder, SharedFile, SharedFolder
from django.contrib.auth.models import User
from .forms import FileForm, FolderForm, SignUpForm
from django.db.models import Q
from django.contrib.auth import login, authenticate
from django.views.decorators.http import require_POST

@login_required
def home(request):
    recent_files = File.objects.filter(owner=request.user).order_by('-uploaded_at')[:3]
    files = File.objects.filter(owner=request.user, is_trash=False).order_by('-updated_at')[:20]
    folders = Folder.objects.filter(owner=request.user, is_trash=False).order_by('-updated_at')[:20]
    return render(request, 'drive/home.html', {'recent_files': recent_files, 'files': files, 'folders': folders})

@login_required
def my_drive(request):
    return home(request)

@login_required
def shared_with_me(request):
    shared_files = SharedFile.objects.filter(shared_with=request.user)
    shared_folders = SharedFolder.objects.filter(shared_with=request.user)
    return render(request, 'drive/shared_with_me.html', {'shared_files': shared_files, 'shared_folders': shared_folders})

@login_required
def recent(request):
    files = File.objects.filter(owner=request.user, is_trash=False, is_spam=False).order_by('-updated_at')[:20]
    folders = Folder.objects.filter(owner=request.user, is_trash=False).order_by('-updated_at')[:20]
    return render(request, 'drive/recent.html', {'files': files, 'folders': folders})

@login_required
def starred(request):
    files = File.objects.filter(owner=request.user, is_starred=True, is_trash=False, is_spam=False)
    folders = Folder.objects.filter(owner=request.user, is_starred=True, is_trash=False)
    return render(request, 'drive/starred.html', {'files': files, 'folders': folders})

@login_required
def trash_list(request):
    files = File.objects.filter(is_trash=True)
    folders = Folder.objects.filter(is_trash=True)
    return render(request, 'drive/trash_list.html', {'files': files, 'folders': folders})

@login_required
def spam(request):
    files = File.objects.filter(owner=request.user, is_spam=True)
    return render(request, 'drive/spam.html', {'files': files})

@login_required
def storage(request):
    total_size = sum(file.file.size for file in File.objects.filter(owner=request.user))
    return render(request, 'drive/storage.html', {'total_size': total_size})

@login_required
def upload_file(request):
    if request.method == 'POST':
        form = FileForm(request.POST, request.FILES)
        if form.is_valid():
            file = form.save(commit=False)
            file.owner = request.user
            file.save()
            return redirect('home')
    else:
        form = FileForm()
    return render(request, 'drive/upload_file.html', {'form': form})

@login_required
def create_folder(request):
    if request.method == 'POST':
        form = FolderForm(request.POST)
        if form.is_valid():
            folder = form.save(commit=False)
            folder.owner = request.user
            folder.save()
            return redirect('home')
    else:
        form = FolderForm()
    return render(request, 'drive/create_folder.html', {'form': form})

@login_required
def folder_detail(request, id):
    folder = get_object_or_404(Folder, id=id)
    return render(request, 'drive/folder_detail.html', {'folder': folder})

@login_required
def share_file(request, file_id):
    file = get_object_or_404(File, id=file_id, owner=request.user)
    if request.method == 'POST':
        username = request.POST.get('username')
        user = User.objects.filter(username=username).first()
        if user:
            SharedFile.objects.create(file=file, shared_with=user)
            return redirect('home')
    return render(request, 'drive/share_file.html', {'file': file})

@login_required
def share_folder(request, folder_id):
    folder = get_object_or_404(Folder, id=folder_id, owner=request.user)
    if request.method == 'POST':
        username = request.POST.get('username')
        user = User.objects.filter(username=username).first()
        if user:
            SharedFolder.objects.create(folder=folder, shared_with=user)
            return redirect('home')
    return render(request, 'drive/share_folder.html', {'folder': folder})

@login_required
def search(request):
    query = request.GET.get('q')
    if query:
        files = File.objects.filter(
            Q(name__icontains=query) & Q(owner=request.user) & Q(is_trash=False) & Q(is_spam=False)
        )
        folders = Folder.objects.filter(
            Q(name__icontains=query) & Q(owner=request.user) & Q(is_trash=False)
        )
    else:
        files = File.objects.none()
        folders = Folder.objects.none()
    return render(request, 'drive/search.html', {'files': files, 'folders': folders, 'query': query})

def signup(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=user.username, password=raw_password)
            login(request, user)
            return redirect('home')
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})

@require_POST
def delete_file(request, file_id):
    file = get_object_or_404(File, id=file_id)
    file.delete()
    return redirect('home')

@require_POST
def delete_folder(request, folder_id):
    folder = get_object_or_404(Folder, id=folder_id)
    folder.delete()
    return redirect('home')

@require_POST
def restore_file(request, file_id):
    file = get_object_or_404(File, id=file_id)
    file.is_trash = False
    file.save()
    return redirect('trash_list')

@require_POST
def restore_folder(request, folder_id):
    folder = get_object_or_404(Folder, id=folder_id)
    folder.is_trash = False
    folder.save()
    return redirect('trash_list')

@require_POST
def delete_file_permanently(request, file_id):
    file = get_object_or_404(File, id=file_id)
    file.delete()
    return redirect('trash_list')

@require_POST
def delete_folder_permanently(request, folder_id):
    folder = get_object_or_404(Folder, id=folder_id)
    folder.delete()
    return redirect('trash_list')

@require_POST
def move_to_trash_file(request, file_id):
    file = get_object_or_404(File, id=file_id)
    file.is_trash = True
    file.save()
    return redirect('home')

@require_POST
def move_to_trash_folder(request, folder_id):
    folder = get_object_or_404(Folder, id=folder_id)
    folder.is_trash = True
    folder.save()
    return redirect('home')
