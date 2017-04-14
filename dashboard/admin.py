from django.contrib import admin
from models import Project, Profile, Student, Teacher, Employer, Course, Enrollment, FormTemplate, Question, FormResponse, QuestionResponse

# Register your models here.
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'type')
class ProjectAdmin(admin.ModelAdmin):
    list_display = ('student', 'title', 'link', 'languagesframeworks', 'image')
class StudentAdmin(admin.ModelAdmin):
    list_display = ('profile', 'privacy_setting', 'created_at', 'updated_at')
class TeacherAdmin(admin.ModelAdmin):
    list_display = ('profile',)
class EmployerAdmin(admin.ModelAdmin):
    list_display = ('profile', 'description')
class CourseAdmin(admin.ModelAdmin):
    list_display = ('name', 'pk')
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'course')
class FormTemplateAdmin(admin.ModelAdmin):
    list_display = ('name', 'course', 'question_list', 'students_allowed', 'teachers_allowed', 'employers_allowed', 'pk')
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('question_text', 'question_type', 'additional_info', 'pk')
class FormResponseAdmin(admin.ModelAdmin):
    list_display = ('form_template', 'user')
class QuestionResponseAdmin(admin.ModelAdmin):
    list_display = ('user', 'question', 'response_text')

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Student, StudentAdmin)
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(Employer, EmployerAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(Enrollment, EnrollmentAdmin)
admin.site.register(FormTemplate, FormTemplateAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(FormResponse, FormResponseAdmin)
admin.site.register(QuestionResponse, QuestionResponseAdmin)
