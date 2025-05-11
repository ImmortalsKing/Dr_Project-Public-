from django.db import models

class SiteSetting(models.Model):
    site_name = models.CharField(max_length=100, verbose_name='نام سایت')
    site_url = models.CharField(max_length=100, verbose_name='دامنه سایت')
    address = models.CharField(max_length=200, verbose_name='آدرس')
    appointment_url = models.CharField(max_length=200, verbose_name='لینک نوبت دهی')
    mobile = models.CharField(max_length=100, null=True, blank=True, verbose_name='موبایل')
    phone = models.CharField(max_length=100, null=True, blank=True, verbose_name='تلفن')
    email = models.CharField(max_length=100, null=True, blank=True, verbose_name='ایمیل')
    copy_right = models.TextField(verbose_name='متن کپی رایت سایت')
    appointment_text = models.TextField(verbose_name='متن بخش رزرو نوبت', null=True, blank=True)
    site_logo = models.ImageField(upload_to='images/site-setting/', verbose_name='لوگو سایت')
    is_main_setting = models.BooleanField(verbose_name='تنظیمات اصلی')

    class Meta:
        verbose_name = 'تنظیمات سایت'
        verbose_name_plural = 'تنظیمات'

    def __str__(self):
        return self.site_name

class NewsletterSubscriber(models.Model):
    email = models.EmailField(unique=True,verbose_name='ایمیل')
    date_subscribed = models.DateTimeField(auto_now_add=True,verbose_name='روز عضویت')

    class Meta:
        verbose_name = 'عضو خبرنامه'
        verbose_name_plural = 'اعضای خبرنامه'

    def __str__(self):
        return self.email

class SiteBanner(models.Model):
    class SiteBannerPosition(models.TextChoices):
        HomePage = 'home-page', 'صفحه اصلی'
        CommonPages = 'common-pages', 'صفحات عمومی'

    title = models.CharField(max_length=200, verbose_name='عنوان')
    url = models.URLField(max_length=400, null=True, blank=True, verbose_name='لینک')
    image = models.ImageField(verbose_name='تصویر', upload_to='images/banners')
    is_active = models.BooleanField(verbose_name='فعال / غیرفعال', default=False)
    position = models.CharField(max_length=200, choices=SiteBannerPosition.choices, verbose_name='جایگاه')

    class Meta:
        verbose_name = 'بنر سایت'
        verbose_name_plural = 'بنرهای سایت'

    def __str__(self):
        return self.title

class SiteImages(models.Model):
    class SiteImagesPosition(models.TextChoices):
        InBanner = 'in banner', 'تصویر داخل بنر'
        AboutDr = 'about dr', 'تصویر قسمت درباره ی پزشک'

    title = models.CharField(max_length=200, verbose_name='عنوان')
    image = models.ImageField(verbose_name='تصویر', upload_to='images/site_images')
    is_active = models.BooleanField(verbose_name='فعال / غیرفعال', default=False)
    position = models.CharField(max_length=200, choices=SiteImagesPosition.choices, verbose_name='جایگاه')

    class Meta:
        verbose_name = 'تصویر سایت'
        verbose_name_plural = 'تصاویر سایت'

    def __str__(self):
        return self.title

class SocialLinks(models.Model):
    title = models.CharField(max_length=200, verbose_name='عنوان')
    whatsapp_url = models.URLField(max_length=300,verbose_name='نشانی واتس اپ')
    instagram_url = models.URLField(max_length=300,verbose_name='نشانی اینستاگرام')
    is_main_urls = models.BooleanField(verbose_name='آیا لینک های اصلی است؟')

    class Meta:
        verbose_name = 'لینک شبکه های اجتماعی'
        verbose_name_plural = 'لینک های شبکه های اجتماعی'

    def __str__(self):
        return self.title