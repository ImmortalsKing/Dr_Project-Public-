from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse
from django.views.generic import TemplateView

from about_module.forms import DrCommentsForm
from about_module.models import Doctor, CommentsAboutDr, ContractedHospitals, WorkingHours
from site_module.models import SiteSetting


class AboutDoctor(TemplateView):
    template_name = 'about_module/about_dr_page.html'

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
        context['doctor'] = Doctor.objects.get(is_main_dr=True)
        working_hours = WorkingHours.objects.filter(doctor__is_main_dr=True)
        context['working_hours'] = sorted(working_hours, key=lambda x: days_order.get(x.day, 7))
        context['setting'] = SiteSetting.objects.get(is_main_setting=True)
        context['comments'] = CommentsAboutDr.objects.order_by('-create_date').filter(parent=None,is_confirmed=True)
        context['comments_count'] = CommentsAboutDr.objects.filter(is_confirmed=True).count()
        context['contracted_hospitals'] = ContractedHospitals.objects.filter(is_active=True, doctor__is_main_dr=True)
        context['form'] = DrCommentsForm()
        return context

    def post(self, request, *args, **kwargs):
        form = DrCommentsForm(request.POST)
        if 'send_comment' in request.POST:
            if form.is_valid():
                subject = form.cleaned_data.get('subject')
                text = form.cleaned_data.get('text')
                parent_id = request.POST.get('parent_id')
                if parent_id is None or parent_id == "":
                    new_comment = CommentsAboutDr(user=request.user, subject=subject, text=text)
                    new_comment.save()
                    messages.success(request, 'نظر شما با موفقیت ثبت شد و پس از تایید مدیر در سایت قرار میگیرد.')
                    return redirect(reverse('about_dr_page'))
                else:
                    parent = CommentsAboutDr.objects.filter(id=parent_id).first()
                    new_comment = CommentsAboutDr(user=request.user, subject=subject, text=text, parent=parent,
                                                  is_confirmed=True)
                    new_comment.save()
                    messages.success(request, 'نظر شما با موفقیت ثبت شد و پس از تایید مدیر در سایت قرار میگیرد.')
                    return redirect(reverse('about_dr_page'))

        elif 'delete' in request.POST:
            comment_id = request.POST.get('delete_comment_id')
            comment = CommentsAboutDr.objects.filter(id=comment_id).first()
            comment.delete()
            return redirect(reverse('about_dr_page'))
        elif 'child_delete' in request.POST:
            comment_id = request.POST.get('cdelete_comment_id')
            comment = CommentsAboutDr.objects.filter(id=comment_id).first()
            comment.delete()
            return redirect(reverse('about_dr_page'))


        context = {
            'form': form
        }
        return render(request, 'about_module/about_dr_page.html', context)