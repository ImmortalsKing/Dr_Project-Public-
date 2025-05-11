from django.contrib import admin

from home_module.models import Services


@admin.register(Services)
class ServicesAdmin(admin.ModelAdmin):
    list_display = ['related_blog', 'is_active']
    list_filter = ['is_active']
    list_editable = ['is_active']
