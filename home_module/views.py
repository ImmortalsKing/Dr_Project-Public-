from django.contrib import messages
from django.db.models import Count
from django.http import Http404
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, View

from about_module.models import CommentsAboutDr, Doctor, WorkingHours, ContractedHospitals
from blog_module.models import Blog
# from home_module.forms import NewsletterSubscriberForm
from home_module.models import Services
from site_module.models import SiteSetting, NewsletterSubscriber, SiteBanner, SiteImages, SocialLinks


# Create your views here.

class HomeView(TemplateView):
    template_name = 'home_module/home_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        if Doctor.objects.filter(is_main_dr=True).exists():
            context['doctor_image'] = Doctor.objects.filter(is_main_dr=True).first().image.url
        context['about_dr_img'] = SiteImages.objects.filter(is_active=True,
                                                              position=SiteImages.SiteImagesPosition.AboutDr).first()
        context['top_banner_img'] = SiteImages.objects.filter(is_active=True,
                                                              position=SiteImages.SiteImagesPosition.InBanner).first()
        context['home_banner'] = SiteBanner.objects.filter(is_active=True,
                                                           position=SiteBanner.SiteBannerPosition.HomePage).first()

        context['services'] = Services.objects.filter(is_active=True)[:6]
        context['reviews'] = CommentsAboutDr.objects.filter(is_confirmed=True, is_show_in_home_page=True).order_by(
            '-create_date')[:5]
        context['blogs'] = Blog.objects.filter(is_active=True).order_by('-created_at').annotate(
            comments_count=Count('blogcomments'))[:3]
        return context


def site_header_component(request):
    social_links = SocialLinks.objects.filter(is_main_urls=True).first()
    common_banner = SiteBanner.objects.filter(is_active=True, position=SiteBanner.SiteBannerPosition.CommonPages).first()
    setting = SiteSetting.objects.filter(is_main_setting=True).first()
    services = Services.objects.filter(is_active=True)
    women_issues_blogs = Blog.objects.filter(is_active=True, is_women_issues=True)
    services_slugs = []
    for service in services:
        services_slugs.append(f'/blogs/{service.related_blog.slug}/')
    women_issues = []
    for blog in women_issues_blogs:
        women_issues.append(f'/blogs/{blog.slug}/')
    desired_path = ''
    desired_path_2 = ''
    if 'register' in request.path:
        desired_path = 'ثبت نام'
    elif 'login' in request.path:
        desired_path = 'ورود به حساب کاربری'
    elif 'forgot-password' in request.path:
        desired_path = 'فراموشی کلمه عبور'
    elif 'reset-password' in request.path:
        desired_path = 'تغییر کلمه عبور'
    elif 'about-dr' in request.path:
        desired_path = 'معرفی پزشک'
    elif 'blogs' in request.path:
        desired_path = 'مقاله(ها)'
    elif 'gallery' in request.path:
        desired_path = 'گالری تصاویر ما'
    elif 'faq' in request.path:
        desired_path = 'سوالات رایج زنان'
    elif 'my-profile' in request.path:
        desired_path = 'پنل کاربری'
    else:
        desired_path = '404'
    context = {
        'desired_path': desired_path,
        'setting': setting,
        'services': services,
        'services_urls': list(services_slugs),
        'women_issues': list(women_issues),
        'women_issues_blogs': women_issues_blogs,
        'common_banner': common_banner,
        'social_links': social_links,
    }
    return render(request, 'shared/header_component.html', context)


def site_footer_component(request):
    days_order = {
        'شنبه': 0,
        'یکشنبه': 1,
        'دوشنبه': 2,
        'سه شنبه': 3,
        'چهارشنبه': 4,
        'پنجشنبه': 5,
        'جمعه': 6,
    }
    setting = SiteSetting.objects.filter(is_main_setting=True).first()
    about_dr = Doctor.objects.filter(is_main_dr=True).first()
    # last_blogs = Blog.objects.order_by('-created_at').filter(is_active=True, is_deleted=False).exclude(
    #     is_services=True)[:5]
    last_blogs = Blog.objects.order_by('-created_at').filter(is_active=True, is_deleted=False)[:5]
    working_hours = WorkingHours.objects.filter(doctor__is_main_dr=True)
    sorted_working_hours = sorted(working_hours, key=lambda x: days_order.get(x.day, 7))
    contracted_hospitals = ContractedHospitals.objects.filter(doctor__is_main_dr=True, is_active=True)
    # form = NewsletterSubscriberForm()
    context = {
        'setting': setting,
        'about_dr': about_dr,
        'last_blogs': last_blogs,
        'working_hours': sorted_working_hours,
        'hospitals': contracted_hospitals,
        # 'form': form,
    }
    return render(request, 'shared/footer_component.html', context)


# class SubscribeToNewsletter(View):
#     def get(self, request):
#         form = NewsletterSubscriberForm()
#         context = {
#             'form': form
#         }
#         return render(request, 'shared/includes/subscribe.html', context)
#
#     def post(self, request):
#         form = NewsletterSubscriberForm(request.POST)
#         if form.is_valid():
#             email = form.cleaned_data.get('email')
#             is_email_exists = NewsletterSubscriber.objects.filter(email=email).exists()
#             if not is_email_exists:
#                 new_subscriber = NewsletterSubscriber.objects.create(email=email)
#                 new_subscriber.save()
#                 messages.success(request, 'شما با موفقیت عضو خبرنامه ما شدید.')
#             else:
#                 messages.info(request, 'شما در حال حاضر عضو خبرنامه هستید.')
#             return redirect(reverse('home_page'))
#         context = {
#             'form': form
#         }
#         return render(request, 'shared/includes/subscribe.html', context)


class RemoveFromNewsletter(View):
    def get(self, request, email):
        is_email_exists = NewsletterSubscriber.objects.filter(email=email).exists()
        if is_email_exists:
            subscriber = NewsletterSubscriber.objects.get(email=email)
            subscriber.delete()
            messages.success(request, 'شما با موفقیت از خبرنامه ما حذف شدید.')
            return redirect(reverse('home_page'))
        else:
            return Http404
