from ckeditor.widgets import CKEditorWidget
from django import forms
from django.core import validators
from django.core.exceptions import ValidationError
from django_recaptcha.fields import ReCaptchaField
from django_recaptcha.widgets import ReCaptchaV2Checkbox

from about_module.models import Doctor, ContractedHospitals, WorkingHours
from account_module.models import User
from blog_module.models import Blog, BlogTags, BlogCategory


class EditProfileForm(forms.ModelForm):
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'mobile', 'email', 'address']
        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'mobile': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
            }),
        }
        error_messages = {
            'email': {
                'required': 'Please enter your email'
            }
        }


class ChangePasswordForm(forms.Form):
    captcha = ReCaptchaField(widget=ReCaptchaV2Checkbox)
    current_password = forms.CharField(
        label='کلمه عبور فعلی: ',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'id': "current-password",
            'name': "current-password",
        }),
        validators=[
            validators.MaxLengthValidator(100)
        ]
    )
    new_password = forms.CharField(
        label='کلمه عبور جدید',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'id': "new-password",
            'name': "new-password",
        }),
        validators=[
            validators.MaxLengthValidator(100)
        ]
    )
    new_password_confirm = forms.CharField(
        label='تائید کلمه عبور جدید',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'id': "new-password-confirm",
            'name': "new-password-confirm",
        }),
        validators=[
            validators.MaxLengthValidator(100)
        ]
    )

    def clean_new_password_confirm(self):
        new_password = self.cleaned_data.get('new_password')
        new_password_confirm = self.cleaned_data.get('new_password_confirm')
        if new_password == new_password_confirm:
            return new_password_confirm
        raise ValidationError('Password and Password confirm are different!')


class CreateNewBlog(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title', 'en_title', 'category', 'image', 'short_description', 'text', 'is_women_issues',
                  'is_services', 'is_active']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'en_title': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'category': forms.Select(attrs={
                'class': 'form-control',
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
            }),
            'short_description': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
            }),
            'text': CKEditorWidget(),
            'is_women_issues': forms.CheckboxInput(attrs={
                'class': 'form-control',
            }),
            'is_services': forms.CheckboxInput(attrs={
                'class': 'form-control',
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-control',
            }),
        }
        error_messages = {
            'title': {
                'required': 'لطفا موضوع را وارد کنید.'
            },
            'en_title': {
                'required': 'لطفا موضوع را به انگلیسی وارد کنید.'
            },
            'category': {
                'required': 'لطفا یک دسته بندی انتخاب کنید.'
            },
            'image': {
                'required': 'لطفا یک تصویر انتخاب کنید.'
            },
            'short_description': {
                'required': 'لطفا متنی کوتاه در توصیف مقاله وارد کنید.'
            },
            'text': {
                'required': 'لطفا محتویات و متن مقاله را وارد کنید.'
            },
        }


class CreateNewBlogTagsForm(forms.ModelForm):
    class Meta:
        model = BlogTags
        fields = ['caption']
        widgets = {
            'caption': forms.TextInput(attrs={
                'class': 'form-control',
            }),
        }
        error_messages = {
            'caption': {
                'required': 'لطفا تگ مورد نظر را وارد کنید.'
            },
        }

    caption = forms.CharField(required=False)


class EditAboutDrForm(forms.ModelForm):
    class Meta:
        model = Doctor
        fields = ['name', 'short_bio', 'biography', 'image']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'short_bio': CKEditorWidget(),
            'biography': CKEditorWidget(),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
            }),
        }
        error_messages = {
            'title': {
                'required': 'لطفا موضوع را وارد کنید.'
            },
            'short_bio': {
                'required': 'لطفا بیوگرافی کوتاهی وارد کنید.'
            },
            'biography': {
                'required': 'لطفا بیوگرافی کامل را وارد کنید.'
            },
            'image': {
                'required': 'لطفا یک تصویر انتخاب کنید.'
            },
        }


class ContractedHospitalsForm(forms.ModelForm):
    class Meta:
        model = ContractedHospitals
        fields = ['full_name', 'is_active']
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'is_active': forms.CheckboxInput(attrs={
                'class': 'form-control',
            }),
        }
        error_messages = {
            'full_name': {
                'required': 'لطفا تگ مورد نظر را وارد کنید.'
            },
            'is_active': {
                'required': 'لطفا فعال بودن را مشخص کنید.'
            },
        }


class WorkingHoursForm(forms.ModelForm):
    class Meta:
        model = WorkingHours
        fields = ['day', 'start_time', 'end_time', 'time_of_day']
        widgets = {
            'day': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'start_time': forms.TimeInput(attrs={
                'class': 'form-control',
            }),
            'end_time': forms.TimeInput(attrs={
                'class': 'form-control',
            }),
            'time_of_day': forms.TextInput(attrs={
                'class': 'form-control',
            }),
        }
        error_messages = {
            'day': {
                'required': 'لطفا روز مورد نظر را وارد کنید.'
            },
            'start_time': {
                'required': 'لطفا زمان شروع را مشخص کنید.'
            },
            'end_time': {
                'required': 'لطفا زمان پایان را مشخص کنید.'
            },
            'time_of_day': {
                'required': 'لطفا موقع مشخص از روز را مشخص کنید.'
            },
        }


class BlogCategoryForm(forms.ModelForm):
    valid_colors = [
        'red', 'blue', 'green', 'yellow', 'purple', 'pink', 'orange', 'black', 'gray', 'brown', 'cyan', 'magenta',
        'lime', 'olive', 'teal', 'navy', 'indigo', 'violet',
    ]
    class Meta:
        model = BlogCategory
        fields = ['title', 'url_title', 'short_description', 'color', 'image']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'url_title': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'short_description': forms.Textarea(attrs={
                'class': 'form-control',
                'row': 3
            }),
            'color': forms.TextInput(attrs={
                'class': 'form-control',
            }),
            'image': forms.FileInput(attrs={
                'class': 'form-control',
            }),
        }
        labels = {
            'color': 'رنگ(استاندارد) به انگلیسی'
        }

    def clean_color(self):
        color = self.cleaned_data.get('color')
        if color.lower() not in self.valid_colors:
            raise forms.ValidationError("رنگ وارد شده معتبر نیست. لطفاً یک رنگ استاندارد وارد کنید.")
        return color