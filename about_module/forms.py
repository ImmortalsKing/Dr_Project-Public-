from django import forms
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox

from about_module.models import CommentsAboutDr


class DrCommentsForm(forms.ModelForm):
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)
    class Meta:
        model = CommentsAboutDr
        fields = ['subject', 'text']
        widgets = {
            'subject': forms.Select(attrs={
                'class': "form-control",
            }),
            'text' : forms.Textarea(attrs={
                'class': "form-control",
            }),
        }
        error_messages = {
            'subject': {
                'required': 'لطفا موضوع مورد نظر خود را انتخاب کنید.'
            },
            'text': {
                'required': 'لطفا متن نظر خود را بنویسید.'
            }
        }