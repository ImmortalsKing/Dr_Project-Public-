# Generated by Django 5.1.6 on 2025-03-09 22:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('about_module', '0015_alter_doctor_name'),
    ]

    operations = [
        migrations.RenameField(
            model_name='contractedhospitals',
            old_name='name',
            new_name='full_name',
        ),
    ]
