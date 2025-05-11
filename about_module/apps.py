from django.apps import AppConfig

import about_module


class AboutModuleConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'about_module'
    verbose_name = 'معرفی پزشک'

    def ready(self):
        import about_module.signals