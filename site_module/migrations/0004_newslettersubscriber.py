# Generated by Django 5.1.6 on 2025-03-22 17:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('site_module', '0003_sitesetting_appointment_url'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewsletterSubscriber',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='ایمیل')),
                ('date_subscribed', models.DateTimeField(auto_now_add=True, verbose_name='روز عضویت')),
            ],
            options={
                'verbose_name': 'عضو خبرنامه',
                'verbose_name_plural': 'اعضای خبرنامه',
            },
        ),
    ]
