from django.shortcuts import render, get_object_or_404, redirect
from django.template.defaultfilters import slugify
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from datetime import datetime
import os.path
from .models import Post
from .forms import UploadForm
from django.http import JsonResponse
from .mypose import OutputPose
from .mypose1 import OutputPoseWebcam
from django.core.files.uploadedfile import InMemoryUploadedFile

def details(req, slug):
    post = get_object_or_404(Post, slug=slug)
    return render(req, 'post/details.html', {'post': post})

def search(req):
    query = req.GET.get('query', '')
    posts = Post.objects.filter(title__icontains=query)
    return render(req, 'post/search.html', {'posts': posts, 'query': query})

def upload_pose(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            pose_image = form.cleaned_data['image']
            filename = default_storage.get_available_name(pose_image.name)
            default_storage.save(filename, ContentFile(pose_image.read()))
            image_bytes, information, title = OutputPose(
                os.path.join(default_storage.location, filename))
            pose_image_2 = InMemoryUploadedFile(ContentFile(image_bytes), None, 'output_image' + datetime.now(
            ).strftime("%d %m %Y %H %M %S") + 'jpg', 'image/jpeg', len(image_bytes), None)
            slug = slugify(
                title + datetime.now().strftime("%d %m %Y %H %M %S"))
            Post.objects.create(user=request.user, title=title, information=information, image=pose_image, detect_image=pose_image_2, slug=slug)
            post = get_object_or_404(Post, slug=slug)

            return render(request, 'post/details.html', {'post': post})
    else:
        form = UploadForm()
    return render(request, 'post/uploadform.html', {'form': form})

def upload_webcam(req):
    if req.method == 'POST':
        pose_result = OutputPoseWebcam()

        # Return the pose result as JSON
        return JsonResponse({'pose_result': pose_result})
    else:
        # Render the form page
        form = UploadForm()
        return render(req, 'post/upload_webcam.html', {'form': form})
    
def delete_pose(req, slug):
    post = Post.objects.get(slug=slug)
    post.delete()
    return redirect('frontpage')