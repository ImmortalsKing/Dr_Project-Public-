# Generated by Django 5.1.6 on 2025-03-22 13:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account_module', '0007_alter_user_address'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(default=False, verbose_name='فعال / غیرفعال'),
        ),
    ]
