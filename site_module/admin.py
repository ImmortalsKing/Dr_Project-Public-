from django.contrib import admin

from site_module import models


@admin.register(models.SiteSetting)
class SiteSettingAdmin(admin.ModelAdmin):
    list_display = ['site_name','site_url','is_main_setting']
    list_filter = ['is_main_setting']

admin.site.register(models.NewsletterSubscriber)
admin.site.register(models.SiteBanner)
admin.site.register(models.SiteImages)
admin.site.register(models.SocialLinks)