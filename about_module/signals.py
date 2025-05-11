from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from about_module.models import Doctor, CommentSubjects


@receiver(m2m_changed, sender=Doctor.services.through)
def sync_services_to_comment_subjects(sender, instance, action, pk_set, **kwargs):
    if action == 'post_add':
        for service_id in pk_set:
            service = instance.services.model.objects.get(pk=service_id)
            blog = service.related_blog
            if blog and blog.title:
                CommentSubjects.objects.get_or_create(subject=blog.title)