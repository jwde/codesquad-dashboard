from django.contrib import admin
from models import Student, Teacher, Employer, Course, Enrollment

# Register your models here.
class StudentAdmin(admin.ModelAdmin):
    list_display = ('profile', 'privacy_setting', 'created_at', 'updated_at')
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('profile',)
class EmployerAdmin(admin.ModelAdmin):
    list_display = ('profile', 'description')
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name',)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course')

admin.site.register(Student, StudentAdmin)
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Employer, EmployerAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Enrollment, EnrollmentAdmin)
