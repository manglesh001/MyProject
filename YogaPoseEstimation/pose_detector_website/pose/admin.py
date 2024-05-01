from django.contrib import admin

from .models import Post

class PostAdmin(admin.ModelAdmin):
    search_fields = ['title', 'information']
    list_display = ['title', 'slug', 'submitted_at']

admin.site.register(Post, PostAdmin)
