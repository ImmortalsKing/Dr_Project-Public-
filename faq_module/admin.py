from django.contrib import admin

from faq_module import models


@admin.register(models.FAQModel)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question',)

@admin.register(models.ContactUs)
class ContactUsAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'subject')