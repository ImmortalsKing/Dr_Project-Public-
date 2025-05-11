from django import forms
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox

from faq_module.models import ContactUs


class ContactUsModelForm(forms.ModelForm):
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)
    class Meta:
        model = ContactUs
        fields = ['full_name', 'email', 'mobile', 'subject', 'message']
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': "نام",
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': "ایمیل",
            }),
            'mobile': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': "شماره تلفن",
            }),
            'subject': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': "موضوع",
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': "پیام",
            }),
        }
        error_messages = {
            'full_name': {
                'required': 'لطفا نام خود را وارد کنید.',
            },
            'email': {
                'required': 'لطفا ایمیل خود را وارد کنید.'
            },
            'subject': {
                'required': 'لطفا موضوع خود را وارد کنید.'
            },
            'mobile': {
                'required': 'لطفا تلفن همراه خود را وارد کنید.'
            },
            'message': {
                'required': 'لطفا متن خود را وارد کنید.'
            },
        }
