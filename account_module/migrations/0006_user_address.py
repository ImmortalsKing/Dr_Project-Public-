# Generated by Django 5.1.6 on 2025-03-07 16:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account_module', '0005_user_email_active_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='address',
            field=models.CharField(blank=True, max_length=300, null=True, verbose_name='آدرس'),
        ),
    ]
