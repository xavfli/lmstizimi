import os
import django
from faker import Faker
from django.contrib.auth import get_user_model
from app_users.models import Student, Teacher

# Django muhitini sozlash
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Conf.settings")  # Loyiha sozlamalarini yuklash
django.setup()

# Faker obyekti yaratish
fake = Faker()

# User modelini olish
User = get_user_model()

def create_fake_users(n=10):
    """ Fake User yaratish """
    for _ in range(n):
        phone = fake.unique.phone_number()
        full_name = fake.name()

        user, created = User.objects.get_or_create(
            phone=phone,
            defaults={"full_name": full_name}
        )
    print(f"{n} ta soxta foydalanuvchi yaratildi!")

def create_fake_teachers(n=5):
    """ Fake Teacher yaratish """
    for _ in range(n):
        full_name = fake.name()
        phone = fake.unique.phone_number()

        user, created = User.objects.get_or_create(
            phone=phone,
            defaults={"full_name": full_name}
        )

        Teacher.objects.create(user=user, full_name=full_name, phone=phone)

    print(f"{n} ta soxta o‘qituvchi yaratildi!")

def create_fake_students(n=10):
    """ Fake Student yaratish """
    for _ in range(n):
        full_name = fake.name()
        phone = fake.unique.phone_number()

        user, created = User.objects.get_or_create(
            phone=phone,
            defaults={"full_name": full_name}
        )

        Student.objects.create(user=user, full_name=full_name, phone=phone)

    print(f"{n} ta soxta talabalar yaratildi!")

if __name__ == "__main__":
    create_fake_users(15)      # 15 ta user yaratamiz
    create_fake_teachers(5)    # 5 ta o'qituvchi yaratamiz
    create_fake_students(10)   # 10 ta talaba yaratamiz
