from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import TemplateView, ListView

from about_module.models import Doctor, WorkingHours
from blog_module.forms import BlogCommentsForm
from blog_module.models import Blog, BlogTags, BlogComments


class BlogDetailsView(TemplateView):
    template_name = 'blog_module/blog_details.html'

    def get_context_data(self, **kwargs):
        days_order = {
            'شنبه': 0,
            'یکشنبه': 1,
            'دوشنبه': 2,
            'سه شنبه': 3,
            'چهارشنبه': 4,
            'پنجشنبه': 5,
            'جمعه': 6,
        }
        context = super().get_context_data(**kwargs)
        blog_slug = self.kwargs.get('slug')
        working_hours = WorkingHours.objects.filter(doctor__is_main_dr=True)
        context['working_hours'] = sorted(working_hours, key=lambda x: days_order.get(x.day, 7))
        context['doctor'] = Doctor.objects.get(is_main_dr=True)
        context['last_blogs'] = Blog.objects.order_by('-created_at').exclude(slug=blog_slug).filter(is_active=True)[:3]
        context['blog'] = Blog.objects.get(slug=blog_slug)
        context['blog_tags'] = BlogTags.objects.filter(blog__slug=blog_slug).all()
        context['comments'] = BlogComments.objects.order_by('-create_date').filter(parent=None,is_confirmed=True,blog__slug=blog_slug)
        context['comments_count'] = BlogComments.objects.filter(is_confirmed=True,blog__slug=blog_slug).count()
        context['form'] = BlogCommentsForm()
        return context

    def post(self, request, *args, **kwargs):
        form = BlogCommentsForm(request.POST)
        if 'send_comment' in request.POST:
            if form.is_valid():
                subject = form.cleaned_data.get('subject')
                text = form.cleaned_data.get('text')
                parent_id = request.POST.get('parent_id')
                blog_slug = kwargs.get('slug')
                blog = Blog.objects.get(slug=blog_slug)
                if parent_id is None or parent_id == "":
                    new_comment = BlogComments(user=request.user, subject=subject, text=text, blog=blog)
                    new_comment.save()
                    messages.success(request, 'نظر شما با موفقیت ثبت شد و پس از تایید مدیر در سایت قرار میگیرد.')
                    return redirect(reverse('blog_details_page', kwargs={'slug': blog_slug}))
                else:
                    parent = BlogComments.objects.filter(id=parent_id).first()
                    new_comment = BlogComments(user=request.user, subject=subject, text=text, parent=parent, blog=blog,
                                               is_confirmed=True)
                    new_comment.save()
                    messages.success(request, 'نظر شما با موفقیت ثبت شد و پس از تایید مدیر در سایت قرار میگیرد.')
                    return redirect(reverse('blog_details_page', kwargs={'slug': blog_slug}))

        elif 'delete' in request.POST:
            blog_slug = kwargs.get('slug')
            comment_id = request.POST.get('delete_comment_id')
            comment = BlogComments.objects.filter(id=comment_id).first()
            comment.delete()
            return redirect(reverse('blog_details_page', kwargs={'slug': blog_slug}))
        elif 'child_delete' in request.POST:
            blog_slug = kwargs.get('slug')
            comment_id = request.POST.get('cdelete_comment_id')
            comment = BlogComments.objects.filter(id=comment_id).first()
            comment.delete()
            return redirect(reverse('blog_details_page', kwargs={'slug': blog_slug}))

        context = {
            'form': form
        }
        return render(request, 'blog_module/blog_details.html', context)

class BlogListView(ListView):
    template_name = 'blog_module/blog_list.html'
    model = Blog
    context_object_name = 'blogs'
    ordering = ['-created_at']
    paginate_by = 6

    def get_queryset(self):
        query = super().get_queryset()
        if 'services' in self.request.path:
            query = query.filter(is_active=True,is_services=True)
        elif 'womens-issues' in self.request.path:
            query = query.filter(is_active=True,is_women_issues=True)
        return query