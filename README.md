# Movie API loyihasi

## Loyihaga umumiy tushuncha
Ushbu loyiha foydalanuvchilar, o'qituvchilar va talabalar bilan ishlash uchun mo'ljallangan backend API hisoblanadi. Django REST Framework (DRF) yordamida ishlab chiqilgan va JWT autentifikatsiya tizimidan foydalanadi.

## Xususiyatlar
- O'qituvchilar: Yangi o'qituvchi yaratish, mavjud o'qituvchilarni boshqarish.
- O'quvchilar: Ro'yxatdan o'tish va tizimga kirish, darslarga yozilish.
- Kurslar: Kurs yaratish, tahrirlash va o'chirish.
- Darslar: Har bir kurs uchun alohida darslarni boshqarish.
- Foydalanuvchi rollari: Administrator, o'qituvchi va o'quvchi rollari mavjud.

## Texnologiyalar
- Python 3.12
- Django 5.1.5
- Django REST Framework
- JWT (JSON Web Token)
- SQLite (yoki boshqa ma'lumotlar bazasi)


## O'rnatish

### Talablar

Loyihani ishga tushirishdan oldin quyidagi dasturlar o'rnatilgan bo'lishi kerak:
- Python 3.10 yoki undan yuqori versiya
- pip (Python paketchisi)
- virtualenv (virtual muhit yaratish uchun)

### Virtual muhitni yaratish va kerakli kutubxonalarni o'rnatish

```bash
python -m venv .venv
source .venv/bin/activate  # Linux yoki MacOS
.venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### Ma'lumotlar bazasini sozlash

```bash
python manage.py migrate
python manage.py createsuperuser  # Admin foydalanuvchisini yaratish
```

### Serverni ishga tushirish

```bash
python manage.py runserver
```

## API Endpointlari

### Autentifikatsiya
- `POST /api/v1/users/register/` - Foydalanuvchini ro'yxatdan o'tkazish
- `POST /token/` - Kirish uchun token olish
- `POST /token/refresh/` - Tokenni yangilash


### Foydalanuvchilar
- `GET /api/v1/users/` - Barcha foydalanuvchilar
- `GET /api/v1/users/{id}/` - Foydalanuvchi ma'lumotlari
- `POST /api/v1/users/` - Yangi foydalanuvchi yaratish
- `PUT /api/v1/users/{id}/` - Foydalanuvchi ma'lumotlarini yangilash
- `DELETE /api/v1/users/{id}/` - Foydalanuvchini o'chirish

## Fake ma'lumotlarni qo'shish (Mock Data)

Loyihaga test ma'lumotlarini qo'shish uchun quyidagi buyruqni ishga tushiring:

```bash
python populate_db.py
```

Bu skript avtomatik ravishda bir nechta foydalanuvchilar, talabalar va o'qituvchilar yaratadi.

## Swagger hujjatlari

API hujjatlarini Swagger orqali ko'rish uchun:

```bash
http://127.0.0.1:8000/swagger/
```

## Muallif
- **Boburbek** - Backend dasturchi

# Loyihani ishlab chiqishda biron muammo yoki taklif bo'lsa, bemalol bog'laning!

# Email
- **email** - nboburbek778@gmail.com

