from django.shortcuts import render
from pose.models import Post

def frontpage(req):
    #posts = Post.objects.all()
    posts = None
    if req.user.is_authenticated:
        posts = Post.objects.filter(user=req.user)
    return render(req, 'core/frontpage.html', {'posts': posts})

def about(req):
    return render(req, 'core/about.html')