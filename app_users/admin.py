from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User,Student,Worker,Course,Teacher,TableType,Group


class UserMainAdmin(UserAdmin):
    list_display = ("phone", "is_student", "is_active", "is_staff")
    ordering = ("phone",)
    search_fields = ("phone",)

    # Agar `AbstractBaseUser` dan foydalansangiz, `fieldsets` ni qo‘lda sozlang
    fieldsets = (
        (None, {"fields": ("phone", "password")}),
        ("Permissions", {"fields": ("is_active", "is_staff", "is_superuser")}),
    )

admin.site.register(User, UserMainAdmin)
admin.site.register(Student)
admin.site.register(Worker)
admin.site.register(Course)
admin.site.register(Teacher)
admin.site.register(TableType)
admin.site.register(Group)