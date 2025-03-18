from django.contrib.auth.base_user import BaseUserManager, AbstractBaseUser
from django.contrib.auth.models import PermissionsMixin, Permission
from django.db import models
from typing import TYPE_CHECKING
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import RegexValidator
import app_users.models
from app_users.models import *
from django.contrib.auth import get_user_model

# User = get_user_model()


if TYPE_CHECKING:
    from app_users.models import Course, Group


class UserManager(BaseUserManager):
    def create_user(self, phone, password=None, **extra_fields):
        if not phone:
            raise ValueError('The Phone number must be set')
        user = self.model(phone=phone, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_admin', True)
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_admin') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        return self.create_user(phone, password, **extra_fields)



class User(AbstractBaseUser, PermissionsMixin):
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,14}$',
                                 message="Phone number must be entered in the format: '+9989012345678'. Up to 14 digits allowed.")
    phone = models.CharField(validators=[phone_regex], max_length=17, unique=True)
    full_name = models.CharField(max_length=50, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=True)
    is_user = models.BooleanField(default=True)
    is_teacher = models.BooleanField(default=True)
    is_student = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)


    USERNAME_FIELD = 'phone'
    REQUIRED_FIELDS = ["full_name"]

    objects = UserManager()

    def __str__(self):
        return self.phone

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, app_label):
        return self.is_admin



class TokenModel(models.Model):
    date = models.DateField()
    token = models.TextField()
    created = models.DateField(auto_now_add=True)

    def __str__(self):
        return str(self.date)


class Worker(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    course = models.ForeignKey('app_users.Course', on_delete=models.CASCADE)
    departments = models.ManyToManyField('Departments', related_name='worker')
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    descriptions = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.user.phone


class Departments(models.Model):
    title = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    descriptions = models.CharField(max_length=500, null=True, blank=True)

    def __str__(self):
        return self.title


class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.SET_NULL, null=True, blank=True , related_name='student')
    phone = models.CharField(validators=[User.phone_regex], max_length=17, unique=True)
    course = models.ForeignKey('app_users.Course', on_delete=models.SET_NULL, null=True, blank=True)
    group = models.ManyToManyField('Group', related_name='student')
    is_line = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    descriptions = models.CharField(max_length=500, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_graduated = models.BooleanField(default=True)

    def __str__(self):
        return self.phone



class Parents(models.Model):
    student = models.OneToOneField(Student, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=50, null=True, blank=True)
    phone_number = models.CharField(max_length=15, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    descriptions = models.CharField(max_length=500, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.full_name



class TableType(models.Model):
    title = models.CharField(max_length=50)
    descriptions = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.title


class Table(models.Model):
    name = models.CharField(max_length=255, unique=True)
    type = models.ForeignKey(TableType, on_delete=models.RESTRICT)
    descriptions = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return self.name


class Course(models.Model):
    name = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.title


class Group(models.Model):
    name = models.CharField(max_length=255, unique=True)
    title = models.CharField(max_length=50, unique=True)
    course = models.ForeignKey('app_users.Course', on_delete=models.CASCADE, null=True, blank=True)
    teacher = models.ManyToManyField(Worker, related_name='teacher')
    table = models.ForeignKey(Table, on_delete=models.RESTRICT)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)
    price = models.CharField(max_length=15, blank=True, null=True)
    descriptions = models.CharField(max_length=500, blank=True, null=True)

    def __str__(self):
        return str(self.name)



class AttendanceLevel(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    teacher = models.ForeignKey('app_users.Teacher', on_delete=models.CASCADE)
    level = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} - {self.level}"




class Attendance(models.Model):
    level = models.ForeignKey(AttendanceLevel, on_delete=models.RESTRICT)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    student = models.ForeignKey(Student, on_delete=models.RESTRICT)
    group = models.ForeignKey(Group, on_delete=models.RESTRICT)

    def __str__(self):
        return self.level


class staff(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, unique=True)
    phone = models.CharField(max_length=17, unique=True)
    email = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name


class Teacher(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    full_name = models.CharField(max_length=50, unique=True)
    phone = models.CharField(max_length=17, unique=True)

    def save(self, *args, **kwargs):
        if not self.user:  # Agar `user` bo‘lmasa, yaratamiz
            self.user = User.objects.create(phone=self.phone, full_name=self.full_name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.full_name



class Commit(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name="commits")
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE)
    text = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.teacher.user.username} -> {self.student.user.username}"


class Payment(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
    ]

    student = models.ForeignKey(User, on_delete=models.CASCADE, related_name="payments")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(max_length=255, unique=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student.username} - {self.amount} - {self.status}"


