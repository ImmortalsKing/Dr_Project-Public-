from django.contrib import admin

from blog_module import models

@admin.register(models.BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ('title', 'is_active', 'is_deleted')
    list_filter = ('is_active', 'is_deleted')
    list_editable = ('is_active', 'is_deleted')

@admin.register(models.Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title','category', 'author', 'created_at', 'is_active', 'is_deleted')
    list_filter = ('is_active', 'is_deleted', 'created_at', 'author', 'category')
    list_editable = ('is_active', 'is_deleted')
    prepopulated_fields = {'slug': ('en_title',)}

@admin.register(models.BlogTags)
class BlogTagsAdmin(admin.ModelAdmin):
    list_display = ('caption','blog')

@admin.register(models.BlogComments)
class BlogCommentsAdmin(admin.ModelAdmin):
    list_display = ('user','blog','create_date','is_confirmed')
    list_editable = ('is_confirmed',)
    list_filter = ('is_confirmed', 'create_date', 'blog', 'user')