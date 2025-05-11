from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField
from django.db import models

from account_module.models import User

class BlogCategory(models.Model):
    title = models.CharField(max_length=100, verbose_name='عنوان')
    url_title = models.CharField(max_length=200, db_index=True, verbose_name='عنوان(انگلیسی)')
    image = models.ImageField(upload_to='images/blogs_categories/', verbose_name='تصویر')
    short_description = models.CharField(max_length=100, verbose_name='توضیحات کوتاه')
    color = models.CharField(max_length=15, verbose_name='رنگ', null=True, blank=True)
    is_active = models.BooleanField(verbose_name='فعال / غیر فعال', default=True)
    is_deleted = models.BooleanField(verbose_name='حذف شده / نشده', default=False)

    class Meta:
        verbose_name = 'دسته بندی مقاله'
        verbose_name_plural = 'دسته بندی های مقالات'

    def __str__(self):
        return self.title

class Blog(models.Model):
    title = models.CharField(max_length=100, verbose_name='عنوان')
    en_title = models.CharField(max_length=100, verbose_name='عنوان به انگلیسی')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='نویسنده')
    category = models.ForeignKey(BlogCategory, on_delete=models.CASCADE, verbose_name='دسته بندی')
    image = models.ImageField(upload_to='images/blog/', verbose_name='تصویر')
    short_description = models.TextField(verbose_name='توضیحات کوتاه')
    text = RichTextUploadingField(verbose_name='متن')
    slug = models.SlugField(max_length=200, db_index=True, unique=True, verbose_name='اسلاگ')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='تاریخ ایجاد')
    is_women_issues = models.BooleanField(default=False, verbose_name='آیا این مقاله جزء دسته ی بیماری ها و مسائل زنان است؟')
    is_services = models.BooleanField(default=False, verbose_name='آیا این مقاله جزء دسته ی خدمات است؟')
    is_active = models.BooleanField(default=True, verbose_name='فعال / غیر فعال')
    is_deleted = models.BooleanField(default=False, verbose_name='حذف شده / نشده')

    class Meta:
        verbose_name = 'مقاله'
        verbose_name_plural = 'مقالات'

    def __str__(self):
        return f'{self.title} / {self.author}'

class BlogTags(models.Model):
    caption = models.CharField(max_length=200,db_index=True,verbose_name='تگ')
    blog = models.ForeignKey(Blog,on_delete=models.CASCADE,related_name='blog_tags',verbose_name='مقاله ی مربوطه')

    class Meta:
        verbose_name = 'تگ بلاگ'
        verbose_name_plural = 'تگ های بلاگ ها'

    def __str__(self):
        return self.caption

class BlogComments(models.Model):
    parent = models.ForeignKey('BlogComments',null=True,blank=True,on_delete=models.CASCADE,related_name="replies", verbose_name='والد کامنت')
    user = models.ForeignKey(User,on_delete=models.CASCADE,verbose_name='کاربر')
    blog = models.ForeignKey(Blog,on_delete=models.CASCADE,verbose_name='مقاله')
    subject = models.CharField(max_length=100,db_index=True,verbose_name='موضوع کامنت')
    text = models.TextField(db_index=True,verbose_name='متن کامنت')
    create_date = models.DateTimeField(auto_now_add=True,verbose_name='تاریخ ارسال')
    is_confirmed = models.BooleanField(verbose_name='تایید شده / نشده',default=False)

    class Meta:
        verbose_name = 'نظر مقاله'
        verbose_name_plural = 'نظرات مقاله ها'

    def __str__(self):
        return f'{self.user} / {self.subject}'