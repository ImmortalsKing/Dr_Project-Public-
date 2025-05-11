from django.db import models

from blog_module.models import Blog


# Create your models here.

class Services(models.Model):
    related_blog = models.OneToOneField(Blog,on_delete=models.CASCADE, verbose_name='مقاله ی مربوطه')
    is_active = models.BooleanField(verbose_name= 'فعال/غیر فعال', default=True)

    def save(self, *args, **kwargs):
        if not self.id:
            existing_ids = set(Services.objects.values_list('id', flat=True))
            all_possible_ids = set(range(1, len(existing_ids) + 2))
            available_ids = sorted(all_possible_ids - existing_ids)
            self.id = available_ids[0]

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'سرویس'
        verbose_name_plural = 'سرویس ها'

    def __str__(self):
        return str(self.related_blog)