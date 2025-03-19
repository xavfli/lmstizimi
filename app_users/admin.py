from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User,Student,Worker,Course,Teacher,TableType,Group,Departments,Table,AttendanceLevel,Payment


class UserMainAdmin(UserAdmin):
    list_display = ("phone", "full_name", "is_active", "is_staff")
    ordering = ("phone",)
    fieldsets = (
        (None, {"fields": ("phone", "password")}),
        ("Personal info", {"fields": ("full_name",)}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser")}),
    )
    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": ("phone", "full_name", "password1", "password2"),
        }),
    )
    search_fields = ("phone", "full_name")


class TeacherAdmin(admin.ModelAdmin):
    list_display = ("full_name", "phone", "user")



admin.site.register(User, UserMainAdmin)
admin.site.register(Student)
admin.site.register(Worker)
admin.site.register(Course)
admin.site.register(Teacher, TeacherAdmin)
admin.site.register(TableType)
admin.site.register(Group)
admin.site.register(Departments)
admin.site.register(Table)
admin.site.register(AttendanceLevel)
admin.site.register(Payment)

