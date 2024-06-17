from django.contrib import admin

from website.models import coordinator

# Register your models here.
class CoordoAdmin(admin.ModelAdmin):
    list_display = ("last_name", "first_name", "is_current")
    list_editable = ("is_current",)
    search_fields = ("last_name", "first_name")

admin.site.register(coordinator, CoordoAdmin)