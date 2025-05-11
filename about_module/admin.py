from django.contrib import admin

from about_module import models


@admin.register(models.Doctor)
class DoctorAdmin(admin.ModelAdmin):
    list_display = ('name', 'is_main_dr')
    list_filter = ('is_main_dr',)
    filter_horizontal = ('services','working_hour','contracted_hospitals')

@admin.register(models.WorkingHours)
class WorkingHoursAdmin(admin.ModelAdmin):
    list_display = ('day','start_time', 'end_time')
    list_filter = ('day',)

@admin.register(models.CommentsAboutDr)
class CommentsAboutDrAdmin(admin.ModelAdmin):
    list_display = ('user', 'subject','create_date','is_confirmed','is_show_in_home_page')
    list_filter = ('subject', 'create_date')
    list_editable = ('is_confirmed','is_show_in_home_page')

admin.site.register(models.CommentSubjects)
admin.site.register(models.ContractedHospitals)
