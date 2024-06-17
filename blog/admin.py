from django.contrib import admin
from blog.models import Blog, Photo, BlogPostImage, Category
from django.contrib import admin

from website.models import coordinator


class BlogPostImageInline(admin.TabularInline):
    model = BlogPostImage
    extra = 1

class BlogPostAdmin(admin.ModelAdmin):
    list_display = ("title", "author", "published", "created_on", "last_updated")
    list_editable = ("published",)
    search_fields = ("title", "content")
    list_filter = ("published", "created_on", "author")
    prepopulated_fields = {"slug": ("title",)}
    ordering = ("-created_on",)
    date_hierarchy = "created_on"
    inlines = [BlogPostImageInline]

admin.site.register(Blog, BlogPostAdmin)
admin.site.register(
    Category,)

# admin.site.register([Blog,
#                      Photo,
#                      ])