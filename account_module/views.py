from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import HttpRequest, Http404
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.generic import View
from django.utils.crypto import get_random_string

from account_module.forms import RegisterForm, LoginForm, ForgotPasswordForm, ResetPasswordForm
from account_module.models import User
from site_module.models import SiteSetting
from utils.email_service import send_email


# Create your views here.

class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        setting = SiteSetting.objects.filter(is_main_setting=True).first()
        context = {
            'register_form': register_form,
            'setting':setting,
        }
        return render(request, 'account_module/register_page.html', context)
    def post(self, request):
        register_form = RegisterForm(request.POST)
        setting = SiteSetting.objects.filter(is_main_setting=True).first()
        site_url = setting.site_url
        if register_form.is_valid():
            first_name = register_form.cleaned_data.get('first_name')
            last_name = register_form.cleaned_data.get('last_name')
            email = register_form.cleaned_data.get('email')
            mobile = register_form.cleaned_data.get('mobile')
            password = register_form.cleaned_data.get('password')
            user_exists = User.objects.filter(email=email).exists()
            if user_exists:
                register_form.add_error('email', 'این ایمیل قبلا ثبت شده است')
            else:
                new_user = User(
                    first_name = first_name,
                    last_name = last_name,
                    email = email,
                    mobile = mobile,
                    username = email,
                    email_active_code = get_random_string(72),
                )
                new_user.set_password(password)
                new_user.save()
                messages.success(request, 'حساب کاربری شما با موفقیت ایجاد شد. جهت فعالسازی حساب خود، به ایمیل خود مراجعه کنید.')
                send_email('فعالسازی حساب کاربری', new_user.email, {'user':new_user,'site_url':site_url}, 'emails/activate_account.html')
                return redirect(reverse('login_page'))
        else:
            pass
        context = {
            'register_form': register_form,
            'setting': setting,
        }
        return render(request, 'account_module/register_page.html', context)

class ActivateAccountView(View):
    def get(self, request: HttpRequest, email_active_code):
        user: User = User.objects.filter(email_active_code__iexact=email_active_code).first()
        if user is not None:
            if not user.is_active:
                user.is_active = True
                user.email_active_code = get_random_string(72)
                user.save()
                messages.success(request, 'اکانت شما فعال شد؛ اکنون می توانید وارد شوید.')
                return redirect(reverse('login_page'))
            else:
                messages.info(request, 'اکانت شما قبلا فعال شده است.')
                return redirect(reverse('login_page'))
        return Http404

class LoginView(View):
    def get(self, request):
        login_form = LoginForm()
        setting = SiteSetting.objects.filter(is_main_setting=True).first()
        context = {
            'login_form': login_form,
            'setting': setting,
        }
        return render(request, 'account_module/login_page.html', context)
    def post(self, request):
        login_form = LoginForm(request.POST)
        setting = SiteSetting.objects.filter(is_main_setting=True).first()
        if login_form.is_valid():
            identifier = login_form.cleaned_data.get('identifier')
            password = login_form.cleaned_data.get('password')
            remember_me = login_form.cleaned_data.get('remember_me', False)
            user = User.objects.filter(username__iexact=identifier).first()
            if not user:
                user = User.objects.filter(mobile__iexact=identifier).first()

            if user and user.check_password(password):
                if user.is_active:
                    login(request, user)
                    if remember_me:
                        if remember_me:
                            request.session.set_expiry(30 * 24 * 60 * 60)
                        else:
                            request.session.set_expiry(0)
                        return redirect(reverse('home_page'))
                else:
                    messages.error(request, 'حساب کاربری شما فعال نیست.')
                    return redirect(reverse('login_page'))
            else:
                messages.error(request, 'شماره همراه، ایمیل و یا رمز عبور اشتباه است.')
                return redirect(reverse('login_page'))
        context = {
            'login_form': login_form,
            'setting': setting,
        }
        return render(request, 'account_module/login_page.html', context)

class ForgotPasswordView(View):
    def get(self, request):
        form = ForgotPasswordForm()
        setting = SiteSetting.objects.filter(is_main_setting=True).first()
        context = {
            'form': form,
            'setting': setting,
        }
        return render(request, 'account_module/forgot_password.html', context)

    def post(self, request):
        form = ForgotPasswordForm(request.POST)
        setting = SiteSetting.objects.filter(is_main_setting=True).first()
        site_url = setting.site_url
        if form.is_valid():
            user_email = form.cleaned_data.get('email')
            user: User = User.objects.filter(email__iexact=user_email).first()
            if user is not None:
                messages.success(request, 'کد بازیابی کلمه عبور برای ایمیل شما ارسال شد.')
                send_email('بازیابی کلمه عبور', user.email, {'user':user,'site_url':site_url}, 'emails/forgot_password.html')
                return redirect(reverse('login_page'))
            else:
                form.add_error('email', 'ایمیل وارد شده صحیح نمی باشد.')
        context = {
            'form': form,
            'setting': setting,
        }
        return render(request, 'account_module/forgot_password.html', context)

class ResetPasswordView(View):
    def get(self, request, active_code):
        setting = SiteSetting.objects.filter(is_main_setting=True).first()
        user: User = User.objects.filter(email_active_code__iexact=active_code).first()
        if user is None:
            return redirect(reverse('login_page'))
        form = ResetPasswordForm()
        context = {
            'form': form,
            'user': user,
            'setting': setting,
        }
        return render(request, 'account_module/reset_password.html', context)

    def post(self, request, active_code):
        setting = SiteSetting.objects.filter(is_main_setting=True).first()
        form = ResetPasswordForm(request.POST)
        user: User = User.objects.filter(email_active_code__iexact=active_code).first()
        if form.is_valid():
            if user is None:
                return redirect(reverse('login_page'))
            user_new_password = form.cleaned_data.get('password')
            user.set_password(user_new_password)
            user.email_active_code = get_random_string(72)
            user.save()
            messages.success(request, 'کلمه عبور شما با موفقیت تغییر یافت.')
            return redirect(reverse('login_page'))
        context = {
            'form': form,
            'user': user,
            'setting': setting,
        }
        return render(request, 'account_module/reset_password.html', context)

@method_decorator(login_required, name='dispatch')
class LogoutView(View):
    def get(self,request):
        logout(request)
        return redirect(reverse('login_page'))
