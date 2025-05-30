from django.apps import AppConfig


class BlogModuleConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'blog_module'
    verbose_name = 'مقالات'

    def ready(self):
        import blog_module.signals
