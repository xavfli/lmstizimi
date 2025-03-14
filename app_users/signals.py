from django.db.models.signals import post_save
from django.dispatch import receiver
from app_users.models import User, Student

@receiver(post_save, sender=User)
def create_student(sender, instance, created, **kwargs):
    if created and instance.is_student:
        Student.objects.create(user=instance)
