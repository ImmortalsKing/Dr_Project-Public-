from django import forms
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox

from about_module.models import CommentsAboutDr
from blog_module.models import BlogComments


class BlogCommentsForm(forms.ModelForm):
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)
    class Meta:
        model = BlogComments
        fields = ['subject', 'text']
        widgets = {
            'subject': forms.TextInput(attrs={
                'class': "form-control",
                'id': 'blog_subject',
                'name': 'blog_subject',
            }),
            'text' : forms.Textarea(attrs={
                'class': "form-control",
            }),
        }
        error_messages = {
            'subject': {
                'required': 'لطفا موضوع مورد نظر خود را بنویسید.'
            },
            'text': {
                'required': 'لطفا متن نظر خود را بنویسید.'
            }
        }