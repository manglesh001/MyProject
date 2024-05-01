from django.db import models
from authuser.models import User

class Post(models.Model):
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)
    title = models.CharField(max_length=255)
    slug = models.SlugField()
    information = models.TextField()
    submitted_at = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)
    detect_image = models.ImageField(upload_to='uploads/', blank=True, null=True)

    class Meta:
        ordering = ('-submitted_at',)
