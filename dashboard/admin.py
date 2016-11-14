from django.contrib import admin
from models import Student, Course, Enrollment

# Register your models here.
class StudentAdmin(admin.ModelAdmin):
    list_display = ('user', 'privacy_setting', 'created_at', 'updated_at')
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name',)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'course', 'start_date')

admin.site.register(Student, StudentAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Enrollment, EnrollmentAdmin)
