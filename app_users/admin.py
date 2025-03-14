from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User,Student,Worker,Course,Teacher,TableType,Group

class UserMainAdmin(UserAdmin):
    list_display = ( 'full_name', 'phone', 'is_active', 'is_staff', 'is_superuser',"is_user","is_teacher","is_student",)
    fieldsets = UserAdmin.fieldsets + (
        ("Additional Info", {
            "fields": ("full_name", "is_user", "is_admin", "is_student"),
        }),
    )
    ordering = ("full_name",)

admin.site.register(User, UserMainAdmin)
admin.site.register(Student)
admin.site.register(Worker)
admin.site.register(Course)
admin.site.register(Teacher)
admin.site.register(TableType)
admin.site.register(Group)