from django.contrib import admin

from gallery_module import models


@admin.register(models.Gallery)
class GalleryAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active')
    list_editable = ('is_active', )