# from django import forms
# from django.core import validators
# from django_recaptcha.fields import ReCaptchaField
# from django_recaptcha.widgets import ReCaptchaV2Checkbox
#
#
# class NewsletterSubscriberForm(forms.Form):
#     email = forms.EmailField(
#         widget=forms.EmailInput(attrs={
#             'name': "EMAIL",
#             'placeholder': "آدرس ایمیل خود را وارد کنید",
#             'required': "",
#             'type': "email",
#         }),
#         validators=[
#             validators.MaxLengthValidator(100),
#             validators.EmailValidator
#         ]
#     )
#     captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)