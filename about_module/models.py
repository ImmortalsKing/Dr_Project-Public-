from ckeditor.fields import RichTextField
from django.db import models

from account_module.models import User
from home_module.models import Services


class WorkingHours(models.Model):
    day = models.CharField(max_length=100, verbose_name='روز')
    start_time = models.TimeField(verbose_name='ساعت شروع')
    end_time = models.TimeField(verbose_name='ساعت پایان')
    time_of_day = models.CharField(max_length=100, verbose_name='موقع از روز(صبح/عصر)')

    class Meta:
        verbose_name = 'زمان کاری'
        verbose_name_plural = 'زمان های کاری'

    def __str__(self):
        return self.day

class ContractedHospitals(models.Model):
    full_name = models.CharField(max_length=300,verbose_name='نام بیمارستان')
    is_active = models.BooleanField(verbose_name='فعال/غیر فعال', default=True)

    class Meta:
        verbose_name = 'بیمارستان'
        verbose_name_plural = 'بیمارستان ها'

    def __str__(self):
        return self.full_name

class Doctor(models.Model):
    name = models.CharField(max_length=200,verbose_name='نام دکتر')
    dr_panel_url = models.URLField(max_length=300,verbose_name='لینک پنل نوبت دهی دکتر')
    image = models.ImageField(upload_to='images/doctor/',verbose_name='تصویر')
    short_bio = RichTextField(verbose_name='بیوگرافی کوتاه')
    biography = RichTextField(verbose_name='بیوگرافی')
    services = models.ManyToManyField(Services, verbose_name='خدمات',null=True,blank=True)
    working_hour = models.ManyToManyField(WorkingHours,verbose_name='ساعات کاری')
    contracted_hospitals = models.ManyToManyField(ContractedHospitals,verbose_name='بیمارستان های طرف قرارداد', null=True,blank=True)
    is_main_dr = models.BooleanField(verbose_name='دکتر اصلی',default=False)

    class Meta:
        verbose_name = 'پزشک'
        verbose_name_plural = 'پزشکان'

    def __str__(self):
        return self.name

class CommentSubjects(models.Model):
    subject = models.CharField(max_length=100,verbose_name='موضوع')

    class Meta:
        verbose_name = 'موضوع کامنت'
        verbose_name_plural = 'موضوعات کامنت ها'

    def __str__(self):
        return self.subject

class CommentsAboutDr(models.Model):
    parent = models.ForeignKey('CommentsAboutDr',null=True,blank=True,on_delete=models.CASCADE,verbose_name='والد کامنت')
    user = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='کاربر')
    subject = models.ForeignKey(CommentSubjects,on_delete=models.CASCADE,verbose_name='موضوع',null=True,blank=True)
    text = models.TextField(db_index=True,verbose_name='متن کامنت')
    create_date = models.DateTimeField(auto_now_add=True,verbose_name='تاریخ ارسال')
    is_confirmed = models.BooleanField(verbose_name='تایید شده / نشده',default=False)
    is_show_in_home_page = models.BooleanField(verbose_name='آیا این دیدگاه در صفحه ی اصلی نمایش داده شود؟',default=False)

    class Meta:
        verbose_name = 'نظر درباره پزشک'
        verbose_name_plural = 'نظرات درباره پزشک'

    def __str__(self):
        return f'{self.user} / {self.subject}'