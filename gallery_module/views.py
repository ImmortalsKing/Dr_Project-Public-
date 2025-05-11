from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import ListView

from gallery_module.models import Gallery


class GalleryView(ListView):
    model = Gallery
    template_name = 'gallery_module/gallery_page.html'
    context_object_name = 'galleries'
    ordering = ['-id']
    paginate_by = 6

    def post(self, request, *args, **kwargs):
        if 'add_img' in request.POST:
            title = request.POST.get('title')
            image = request.FILES.get('image')
            new_gallery = Gallery(title=title, image=image)
            new_gallery.save()
            messages.success(request, 'تصویر با موفقیت اضافه شد')
            return redirect(reverse('gallery_page'))
        elif 'delete_gallery' in request.POST:
            img_id = request.POST.get('img_id')
            selected_gallery = Gallery.objects.get(id=img_id)
            selected_gallery.delete()
            messages.success(request, 'تصویر با موفقیت حذف شد')
            return redirect(reverse('gallery_page'))