from django.db import models

class Gallery(models.Model):
    title = models.CharField(max_length= 100, verbose_name= 'عنوان تصویر')
    image = models.ImageField(upload_to= 'images/gallery/', verbose_name= 'تصویر')
    is_active = models.BooleanField(default= True, verbose_name= 'فعال / غیر فعال')

    class Meta:
        verbose_name = 'گالری تصویر'
        verbose_name_plural = 'گالری تصاویر'

    def __str__(self):
        return self.title