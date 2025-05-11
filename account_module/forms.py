from django import forms
from django.core import validators
from django.core.exceptions import ValidationError
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox


class RegisterForm(forms.Form):
    first_name = forms.CharField(
        label='نام',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': "نام",
        }),
        validators=[
            validators.MaxLengthValidator(100),
        ]
    )
    last_name = forms.CharField(
        label='نام خانوادگی',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': "نام خانوادگی",
        }),
        validators=[
            validators.MaxLengthValidator(100),
        ]
    )
    email = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': "ایمیل",
        }),
        validators=[
            validators.MaxLengthValidator(100),
            validators.EmailValidator
        ]
    )
    mobile = forms.IntegerField(
        label='شماره همراه',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': "شماره همراه",
        }),
    )
    password = forms.CharField(
        label= 'کلمه عبور',
        widget= forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': "کلمه عبور",
        }),
        validators=[
            validators.MaxLengthValidator(100),
        ]
    )
    password_confirm = forms.CharField(
        label= 'تایید کلمه عبور',
        widget= forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': "تایید کلمه عبور",
        }),
        validators=[
            validators.MaxLengthValidator(100),
        ]
    )
    captcha = ReCaptchaField(widget= ReCaptchaV2Checkbox)

    def clean_password_confirm(self):
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')
        if password == password_confirm:
            return password_confirm
        raise ValidationError('کلمه عبور و تایید کلمه عبور با هم مغایرت دارند.')


class LoginForm(forms.Form):
    identifier = forms.CharField(
        label='شماره همراه یا ایمیل',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'شماره همراه یا ایمیل',
        }),
        validators=[
            validators.MaxLengthValidator(100)
        ]
    )
    password = forms.CharField(
        label='کلمه عبور',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'کلمه عبور'
        }),
        validators=[
            validators.MaxLengthValidator(100)
        ]
    )
    remember_me = forms.BooleanField(
        required=False,
        label='مرا به خاطر بسپار',
        widget=forms.CheckboxInput(attrs={'class':'form-check-input'})
    )
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)

class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(
        label='ایمیل',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': "ایمیل خود را وارد کنید",
        }),
        validators=[
            validators.MaxLengthValidator(100),
            validators.EmailValidator
        ]
    )
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)

class ResetPasswordForm(forms.Form):
    password = forms.CharField(
        label='کلمه عبور جدید',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': "کلمه عبور جدید",
        }),
        validators=[
            validators.MaxLengthValidator(100),
        ]
    )
    password_confirm = forms.CharField(
        label='تائید کلمه عبور جدید',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': "تائید کلمه عبور جدید",
        }),
        validators=[
            validators.MaxLengthValidator(100),
        ]
    )
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)

    def clean_password_confirm(self):
        password = self.cleaned_data.get('password')
        password_confirm = self.cleaned_data.get('password_confirm')
        if password == password_confirm:
            return password_confirm
        raise ValidationError('کلمه عبور جدید و تائید کلمه عبور جدید با هم مغایرت دارند.')