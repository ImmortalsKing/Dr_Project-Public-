from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from about_module.models import Doctor
from blog_module.models import Blog
from home_module.models import Services
from site_module.models import NewsletterSubscriber, SiteSetting
from utils.email_service import send_email

@receiver(post_save, sender=Blog)
def add_to_dr_services(sender, instance, created, **kwargs):
    if created and instance.is_active and instance.is_services:
        try:
            doctor = Doctor.objects.get(is_main_dr=True)
            service, _ = Services.objects.get_or_create(related_blog=instance, defaults={'is_active': True})
            doctor.services.add(service)
        except Doctor.DoesNotExist:
            pass


@receiver(post_save,sender=Blog)
def send_blog_notification(sender, instance, created, **kwargs):
    if created and instance.is_active:
        site_settings = SiteSetting.objects.filter(is_main_setting=True).first()
        subscribers = NewsletterSubscriber.objects.all()
        recipient_emails = [subscriber.email for subscriber in subscribers]

        for email in recipient_emails:
            context = {
                'title': instance.title,
                'short_description': instance.short_description,
                'url': f'{site_settings.site_url}/blogs/{instance.slug}',
                'email': email,
                'site_logo': f'{site_settings.site_url}{settings.STATIC_URL}images/main_logo.png',
                'site_url': site_settings.site_url
            }
            send_email(f'مطلب جدید با عنوان "{instance.title}"',to=email,context=context,template_name='emails/newsletter.html')