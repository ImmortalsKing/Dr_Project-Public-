from django.db import models


class FAQModel(models.Model):
    question = models.TextField(verbose_name='سوال')
    answer = models.TextField(verbose_name='پاسخ')

    class Meta:
        verbose_name = 'پرسش و پاسخ'
        verbose_name_plural = 'پرسش و پاسخ ها'

    def __str__(self):
        return self.question


class ContactUs(models.Model):
    full_name = models.CharField(max_length=200, verbose_name='نام و نام خانوادگی')
    email = models.EmailField(max_length=200, verbose_name='ایمیل')
    mobile = models.CharField(max_length=200, verbose_name='موبایل')
    subject = models.CharField(max_length=200, db_index=True, verbose_name='موضوع')
    message = models.TextField(verbose_name='متن')
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    response = models.TextField(verbose_name='پاسخ', null=True, blank=True)
    is_read_by_admin = models.BooleanField(default=False, verbose_name='آیا توسط ادمین دیده شده است؟')

    class Meta:
        verbose_name = 'ارتباط با ما'
        verbose_name_plural = 'ارتباط با ما'

    def __str__(self):
        return f'{self.subject} / {self.full_name}'
