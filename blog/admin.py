from django.contrib import admin
from blog.models import Blog, Photo
from blog.views import deletephoto, photo_upload

# Register your models here.
admin.site.register([Blog,
                     Photo,
                     ])