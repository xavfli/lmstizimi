import os
import django
from faker import Faker
from app_users.models import Teacher
from django.contrib.auth import get_user_model

# Django muhitini sozlash
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Conf.settings")
django.setup()

# Faker obyekti yaratish
fake = Faker()

# User modelini olish
User = get_user_model()


def create_fake_teachers(n=10):
    for _ in range(n):
        full_name = fake.name()
        phone = fake.phone_number()

        # User yaratish yoki borini olish
        user, created = User.objects.get_or_create(phone=phone, defaults={"full_name": full_name})

        # Teacher yaratish
        Teacher.objects.create(user=user, full_name=full_name, phone=phone)

    print(f"{n} ta soxta o‘qituvchi yaratildi!")


if __name__ == "__main__":
    create_fake_teachers(10)
