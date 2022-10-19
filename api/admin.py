from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import Course, Student, Question, QComment, CComment, Like
from .models import User

# Register your models here.admin.site.register(Vote)
admin.site.register(Student)
admin.site.register(Question)
admin.site.register(Course)
admin.site.register(QComment)
admin.site.register(CComment)
admin.site.register(Like)

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": ("username", "password1", "password2", 'email', 'first_name', 'last_name'),
            },
        ),
    )


class StudentAdmin(admin.ModelAdmin):
    list_display = ['first_name', 'last_name', 'id', 'email']
    list_editable = ['first_name', 'last_name']
    list_per_page = 10
    list_select_related = ['user']
    ordering = ['user__first_name', 'user__last_name']
    search_fields = ['first_name__istartwith', 'last_name_istartwith']

    
    
