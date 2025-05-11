from django.contrib import messages
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views.generic import TemplateView, CreateView, View

from faq_module.forms import ContactUsModelForm
from faq_module.models import FAQModel


class FaqView(View):
    def get(self, request):
        contact_form = ContactUsModelForm()
        faqs = FAQModel.objects.all()
        context = {
            'contact_form': contact_form,
            'faqs': faqs,
        }
        return render(request, 'faq_module/faq_page.html', context)
    def post(self, request):
        contact_form = ContactUsModelForm(request.POST)
        faqs = FAQModel.objects.all()
        if "contact_btn" in request.POST:
            if contact_form.is_valid():
                contact_form.save()
                messages.success(request, 'پیام شما با موفقیت ارسال شد. با تشکر')
                return redirect(reverse("faq_page"))
            else:
                messages.error(request, 'در هنگام ارسال پیام خطایی رخ داده است.')
        elif "add_faq" in request.POST:
            question = request.POST.get('question')
            answer = request.POST.get('answer')
            new_faq = FAQModel(question=question, answer=answer)
            new_faq.save()
            messages.success(request, 'پرسش و پاسخ شما با موفقیت اضافه شد.')
            return redirect(reverse("faq_page"))
        elif "delete_faq" in request.POST:
            faq_id = request.POST.get('faq_id')
            selected_faq = FAQModel.objects.get(id=faq_id)
            selected_faq.delete()
            messages.success(request, 'پرسش و پاسخ مورد نظر با موفقیت حذف شد.')
            return redirect(reverse("faq_page"))
        context = {
            'contact_form': contact_form,
            'faqs': faqs,
        }
        return render(request, "faq_module/faq_page.html", context)