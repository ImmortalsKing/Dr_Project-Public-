from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponseRedirect, Http404
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.utils.decorators import method_decorator
from django.utils.text import slugify
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, View, ListView, CreateView, UpdateView

from about_module.models import CommentsAboutDr, Doctor, ContractedHospitals, WorkingHours
from account_module.models import User
from blog_module.models import BlogComments, Blog, BlogTags, BlogCategory
from home_module.models import Services
from user_panel_module.forms import EditProfileForm, ChangePasswordForm, CreateNewBlogTagsForm, ContractedHospitalsForm, \
    WorkingHoursForm, BlogCategoryForm


@method_decorator(login_required, name='dispatch')
class MyProfileView(TemplateView):
    template_name = 'user_panel_module/my_profile_page.html'


@method_decorator(login_required, name='dispatch')
class EditProfileView(View):
    def get(self, request):
        current_user = User.objects.get(id=request.user.id)
        edit_form = EditProfileForm(instance=current_user)
        pass_form = ChangePasswordForm()
        context = {
            'edit_form': edit_form,
            'pass_form': pass_form,
        }
        return render(request, 'user_panel_module/edit_profile_page.html', context)

    def post(self, request):
        current_user = User.objects.get(id=request.user.id)
        edit_form = EditProfileForm(request.POST, instance=current_user)
        pass_form = ChangePasswordForm(request.POST)

        if 'edit_profile_btn' in request.POST:
            if edit_form.is_valid():
                edit_form.save(commit=True)
                messages.success(request, 'تغییرات پروفایل با موفقیت اعمال شد.')
                return redirect(reverse('my_profile_page'))
            else:
                messages.error(request, 'تغییرات پروفایل با خطا مواجه شد. لطفا مجددا تلاش کنید.')
        elif 'change_pass_btn' in request.POST:
            if pass_form.is_valid():
                current_password = pass_form.cleaned_data.get('current_password')
                new_password = pass_form.cleaned_data.get('new_password')
                if current_user.check_password(current_password):
                    current_user.set_password(new_password)
                    current_user.save()
                    messages.success(request, 'کلمه عبور با موفقیت تغییر کرد. لطفا مجددا وارد شوید.')
                    return redirect(reverse('login_page'))
                else:
                    messages.error(request, 'کلمه عبور فعلی اشتباه است.')
            else:
                messages.error(request, 'تغییر کلمه عبور با خطا مواجه شد. لطفا مجددا تلاش کنید.')
        context = {
            'edit_form': edit_form,
            'pass_form': pass_form,
        }
        return render(request, 'user_panel_module/edit_profile_page.html', context)


class ProfileSidebarComponent(TemplateView):
    template_name = 'components/profile_sidebar_component.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['main_doctor'] = Doctor.objects.filter(is_main_dr=True).first()
        return context


@login_required
def upload_avatar(request):
    if request.method == 'POST':
        if 'avatar' in request.FILES:
            request.user.avatar = request.FILES['avatar']
            request.user.save()
        else:
            pass
    return redirect(request.META.get('HTTP_REFERER', '/'))


@method_decorator(login_required, name='dispatch')
class AboutDrCommentsView(ListView):
    template_name = 'user_panel_module/About_Dr_comments_list_page.html'
    model = CommentsAboutDr
    context_object_name = 'comments'
    paginate_by = 6
    ordering = '-create_date'

    def post(self, request, *args, **kwargs):
        if 'confirm_comment_btn' in request.POST:
            selected_comment_id = request.POST.get('selected_comment_id')
            selected_comment = CommentsAboutDr.objects.get(id=selected_comment_id)
            selected_comment.is_confirmed = True
            selected_comment.save()
            return redirect(f"/about-dr/#comment_{selected_comment.id}")


@method_decorator(login_required, name='dispatch')
class BlogsCommentsView(ListView):
    template_name = 'user_panel_module/blogs_comments_list_page.html'
    model = BlogComments
    context_object_name = 'comments'
    paginate_by = 6
    ordering = '-create_date'

    def post(self, request, *args, **kwargs):
        if 'confirm_comment_btn' in request.POST:
            selected_comment_id = request.POST.get('selected_comment_id')
            selected_comment = BlogComments.objects.get(id=selected_comment_id)
            selected_comment.is_confirmed = True
            selected_comment.save()
            return redirect(f"/blogs/{selected_comment.blog.slug}/#comment_{selected_comment.id}")


@method_decorator(login_required, name='dispatch')
class BlogsListPanelView(ListView):
    template_name = 'user_panel_module/blogs_list_panel.html'
    model = Blog
    context_object_name = 'blogs'
    paginate_by = 6
    ordering = '-created_at'


@method_decorator(login_required, name='dispatch')
class CreateNewBlogView(CreateView):
    template_name = 'user_panel_module/create_new_blog.html'
    model = Blog
    fields = ['title', 'en_title', 'category', 'image', 'short_description', 'text', 'is_women_issues', 'is_services',
              'is_active']

    def form_valid(self, form):
        en_title = form.cleaned_data.get('en_title')
        if en_title:
            form.instance.slug = slugify(en_title)
        form.instance.author = self.request.user
        response = super().form_valid(form)

        is_services = form.cleaned_data.get('is_services')
        is_active = form.cleaned_data.get('is_active')

        tags_form = CreateNewBlogTagsForm(self.request.POST)
        if tags_form.is_valid():
            captions = tags_form.cleaned_data.get('caption')
            if captions:
                tag_list = [tag.strip() for tag in captions.split(',')]
                for caption in tag_list:
                    BlogTags.objects.create(caption=caption, blog=self.object)

        messages.success(self.request, 'مقاله با موفقیت ثبت شد.')
        return response

    def form_invalid(self, form):
        messages.error(self.request, 'متاسفانه مقاله ایجاد نشد. لطفا مجددا تلاش کنید.')
        return super().form_invalid(form)

    def get_success_url(self):
        return reverse('blogs_list_panel_page')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tags_form'] = CreateNewBlogTagsForm()
        return context


@method_decorator(login_required, name='dispatch')
class EditBlogView(UpdateView):
    template_name = 'user_panel_module/edit_blog.html'
    model = Blog
    fields = ['title', 'en_title', 'category', 'image', 'short_description', 'text', 'is_women_issues', 'is_services',
              'is_active']
    success_url = reverse_lazy('blogs_list_panel_page')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        blog = self.get_object()
        context['blog'] = blog
        context['tags_form'] = CreateNewBlogTagsForm(
            initial={'caption': ', '.join(tag.caption for tag in blog.blog_tags.all())})
        context['existing_tags'] = blog.blog_tags.all()
        return context

    def get_object(self, queryset=None):
        slug = self.kwargs.get('slug')
        return get_object_or_404(Blog, slug=slug)

    def form_valid(self, form):
        action = self.request.POST.get('action')

        if action == 'edit':
            en_title = form.cleaned_data.get('en_title')
            if en_title:
                form.instance.slug = slugify(en_title)
            tags_form = CreateNewBlogTagsForm(self.request.POST)
            if tags_form.is_valid():
                captions = tags_form.cleaned_data.get('caption')
                if captions:
                    BlogTags.objects.filter(blog=form.instance).delete()
                    tag_list = [tag.strip() for tag in captions.split(',')]
                    for caption in tag_list:
                        BlogTags.objects.create(caption=caption, blog=form.instance)

            messages.success(self.request, 'مقاله با موفقیت ویرایش شد.')
            return super().form_valid(form)

        elif action == 'delete':
            blog = form.instance
            blog.delete()
            messages.success(self.request, 'مقاله با موفقیت حذف شد.')
            return HttpResponseRedirect(self.success_url)

        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'متاسفانه مقاله ویرایش نشد. لطفا مجددا تلاش کنید.')
        return super().form_invalid(form)


class EditAboutDr(UpdateView):
    template_name = 'user_panel_module/edit_about_dr_page.html'
    model = Doctor
    fields = ['name', 'short_bio', 'biography', 'image']

    # success_url = reverse_lazy('my_profile_page')

    def get_object(self, queryset=None):
        pk = self.kwargs.get('pk')
        return get_object_or_404(Doctor, pk=pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        doctor = self.get_object()
        context['doctor'] = doctor
        context['hospitals_form'] = ContractedHospitalsForm(
            initial={'full_name': ', '.join(hospital.full_name for hospital in doctor.contracted_hospitals.all())})
        context['existing_hospitals'] = doctor.contracted_hospitals.all()
        context['working_hours_list'] = doctor.working_hour.all()
        return context

    def form_valid(self, form):
        doctor = form.save(commit=False)
        doctor.save()

        hospitals_form = ContractedHospitalsForm(self.request.POST)
        if hospitals_form.is_valid():
            hospitals = hospitals_form.cleaned_data.get('full_name')
            if hospitals:
                doctor.contracted_hospitals.clear()
                hospital_list = [hospital.strip() for hospital in hospitals.split(',')]
                for hospital_name in hospital_list:
                    hospital, created = ContractedHospitals.objects.get_or_create(full_name=hospital_name)
                    doctor.contracted_hospitals.add(hospital)

        messages.success(self.request, 'بخش "معرفی پزشک" با موفقیت ویرایش شد.')
        return super().form_valid(form)


    def form_invalid(self, form):
        messages.error(self.request, 'متاسفانه بخش "معرفی پزشک" ویرایش نشد. لطفا مجددا تلاش کنید.')
        return super().form_invalid(form)


    def get_success_url(self):
        return reverse('about_doctor_edit', kwargs={'pk': self.object.pk})


class CreateWorkingHoursView(TemplateView):
    template_name = 'user_panel_module/create_working_hour.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['working_hour_form'] = WorkingHoursForm()
        doctor = Doctor.objects.get(is_main_dr=True)
        context['doctor'] = doctor
        context['working_hours_list'] = doctor.working_hour.all()
        return context

    def post(self, request, *args, **kwargs):
        if 'add_working_hour' in request.POST:
            working_hour_form = WorkingHoursForm(self.request.POST)
            if working_hour_form.is_valid():
                working_hour = working_hour_form.save(commit=False)
                working_hour.save()

                doctor = Doctor.objects.get(is_main_dr=True)
                doctor.working_hour.add(working_hour)
                doctor.save()

                messages.success(request, 'ساعت کاری جدید با موفقیت ثبت شد.')
                return redirect(reverse('create_working_hours'))
            else:
                messages.error(request, 'خطا در فرم! لطفاً اطلاعات را بررسی کنید.')
                return redirect(reverse('create_working_hours'))
        elif 'delete_wh' in request.POST:
            time_id = request.POST.get('time_id')
            working_hour = WorkingHours.objects.get(id=time_id)
            working_hour.delete()
            messages.success(request, 'ساعت کاری با موفقیت حذف شد.')
            return redirect(reverse('create_working_hours'))


class BlogCategoryView(TemplateView):
    template_name = 'user_panel_module/create_blog_category.html'

    def get_context_data(self, **kwargs):
        valid_colors = [
            'red', 'blue', 'green', 'yellow', 'purple', 'pink', 'orange', 'black', 'gray', 'brown', 'cyan', 'magenta',
            'lime', 'olive', 'teal', 'navy', 'indigo', 'violet',
        ]
        context = super().get_context_data(**kwargs)
        context['valid_colors'] = valid_colors
        context['blog_category_form'] = BlogCategoryForm()
        context['blog_category_list'] = BlogCategory.objects.filter(is_active=True, is_deleted=False)
        return context

    def post(self, request, *args, **kwargs):
        if 'add_blog_category' in request.POST:
            blog_category_form = BlogCategoryForm(self.request.POST, self.request.FILES)
            if blog_category_form.is_valid():
                working_hour = blog_category_form.save(commit=False)
                working_hour.save()

                messages.success(request, 'دسته بندی جدید با موفقیت ثبت شد.')
                return redirect(reverse('create_blog_category'))
            else:
                messages.error(request, 'خطا در فرم! لطفاً اطلاعات را بررسی کنید.')
                return redirect(reverse('create_blog_category'))
        elif 'delete_blog_category' in request.POST:
            category_id = request.POST.get('category_id')
            category = BlogCategory.objects.get(id=category_id)
            category.delete()
            messages.success(request, 'دسته بندی با موفقیت حذف شد.')
            return redirect(reverse('create_blog_category'))


class CommentsFilterComponent(TemplateView):
    template_name = 'components/comments_filter_component.html'
