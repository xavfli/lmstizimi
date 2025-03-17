from django.core.cache import cache
from django.utils.dateparse import parse_date
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAdminUser
# from rest_framework.request.Request import user
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from .serializers import *
from django.contrib.auth.hashers import make_password
from rest_framework.viewsets import ModelViewSet
from app_users.models import *
from app_users.pagination import CustomPagination
import random
from .models import User
from django.db.models import Min,Max


class PhoneSendOTP(APIView):
    @swagger_auto_schema(request_body=SMSSerializer)
    def post(self, request, *args, **kwargs):
        phone_number = request.data.get('phone_number')
        print(phone_number)
        if phone_number:
            phone = str(phone_number)
            user = User.objects.filter(phone__iexact=phone)
            if user.exists():
                return Response({
                    'status': False,
                    'detail': 'phone number already exist'
                })
            else:
                key = send_otp(phone)

                if key:
                    # Store the verification code and phone number in cache for 5 minutes
                    cache.set(phone_number, key, 600)

                    return Response({"message": "SMS sent successfully"}, status=status.HTTP_200_OK)

                return Response({"message": "Failed to send SMS"}, status=status.HTTP_400_BAD_REQUEST)


def send_otp(phone):
    if phone:
        result = "".join(str(random.randint(1, 9)) for _ in range(4))
        print(result)
        return result
    else:
        return False


class VerifySms(APIView):
    pagination_class = PageNumberPagination

    @swagger_auto_schema(request_body=VerifySMSSerializer)
    def post(self, request):
        serializer = VerifySMSSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            verification_code = serializer.validated_data['verification_code']
            cached_code = str(cache.get(phone_number))
            if verification_code == str(cached_code):
                return Response({
                    'status': True,
                    'detail': 'OTP matched. please proceed for registration'
                })
            else:
                return Response({
                    'status': False,
                    'detail': 'otp INCOORECT'
                })
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegisterUserApi(APIView):
    pagination_class = PageNumberPagination

    @swagger_auto_schema(request_body=UserSerializer)
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            password = serializer.validated_data.get('password')
            serializer.validated_data['password'] = make_password(password)
            serializer.save()

            if User.is_student:
                Student.objects.create(user=User)


            return Response({
                'status': True,
                'datail': 'Account create'
            })

    def get(self, request):
        users = User.objects.all().order_by('-id')
        serializer = UserSerializer(users, many=True)
        return Response(data=serializer.data)


class ChangePasswordView(APIView):
    permission_classes = (permissions.IsAuthenticated,)

    @swagger_auto_schema(request_body=ChangePasswordSerializer)
    def patch(self, request, *args, **kwargs):
        serializer = ChangePasswordSerializer(instance=self.request.user, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DepartmentsApiView(ModelViewSet):
    queryset = Departments.objects.all().order_by('-id')
    serializer_class = DepartmentsSerializer
    pagination_class = PageNumberPagination


# class TeacherApiView(APIView):
#     pagination_class = PageNumberPagination
#
#     @swagger_auto_schema(request_body=WorkerSerializer)
#     def post(self, request):
#         serializer = WorkerSerializer(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             user_id = str(serializer.validated_data.get('user'))
#             try:
#                 user = User.objects.get(phone=user_id)
#                 user.is_teacher = 1
#                 user.save()
#                 serializer.save()
#
#             except Exception as e:
#                 print(e)
#             return Response(data=serializer.data)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def get(self, request):
#         teacher = Worker.objects.filter(user__is_teacher=True).order_by('-id')
#         serializer = WorkerSerializer(instance=teacher, many=True)
#         return Response(data=serializer.data)


class TeacherApiView(APIView):
    pagination_class = PageNumberPagination

    @swagger_auto_schema(request_body=WorkerSerializer)
    def post(self, request):
        serializer = WorkerSerializer(data=request.data)
        if serializer.is_valid():
            user_id = str(serializer.validated_data.get('user'))
            try:
                user = User.objects.get(phone=user_id)
                user.is_teacher = True
                user.save()
                serializer.save()
                return Response(data=serializer.data, status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class TeacherListApiView(APIView):
    def get(self, request):
        teachers = Worker.objects.filter(user__is_teacher=True).order_by('-id')
        serializer = WorkerSerializer(teachers, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)



class TeacherGroupsView(APIView):
    def get(self, request, teacher_id):
        try:
            teacher = Teacher.objects.get(id=teacher_id)
            groups = teacher.groups.all()
            serializer = GroupSerializer(groups, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Teacher.DoesNotExist:
            return Response({"error": "Teacher not found"}, status=status.HTTP_404_NOT_FOUND)




class WorkerApiView(APIView):
    pagination_class = PageNumberPagination

    @swagger_auto_schema(request_body=WorkerSerializer)
    def post(self, request):
        serializer = WorkerSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            worker = Worker.objects.create(
                phone=serializer.validated_data.get('phone'),
                full_name=serializer.validated_data.get('full_name'),
                course=serializer.validated_data.get('course'),
                departments=serializer.validated_data.get('departments'),
                descriptions=serializer.validated_data.get('descriptions')
            )
            return Response(WorkerSerializer(worker).data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        workers = Worker.objects.all().order_by('-id')
        serializer = WorkerSerializer(workers, many=True)
        return Response(data=serializer.data)


class WorkerApiViewId(APIView):
    def get(self, request, pk):
        try:
            worker = Worker.objects.get(pk=pk)
            serializer = WorkerSerializer(worker)
            return Response(data=serializer.data)
        except Worker.DoesNotExist:
            return Response(data={'error': 'Worker not found'}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        try:
            worker = Worker.objects.get(pk=pk)
            serializer = WorkerSerializer(worker, data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(data=serializer.data)
        except Worker.DoesNotExist:
            return Response(data={'error': 'Worker not found'}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, pk):
        try:
            worker = Worker.objects.get(pk=pk)
            serializer = WorkerSerializer(worker, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(data=serializer.data)
        except Worker.DoesNotExist:
            return Response(data={'error': 'Worker not found'}, status=status.HTTP_404_NOT_FOUND)



# class StudentApiView(APIView):
#     pagination_class = CustomPagination
#
#     @swagger_auto_schema(request_body=StudentSerializer)
#     def post(self, request):
#         serializer = StudentSerializer(data=request.data)
#         if serializer.is_valid(raise_exception=True):
#             user_id = serializer.validated_data.get('user')
#             user = User.objects.get(phone=user_id)
#             user.is_student = True
#             user.save()
#             serializer.save()
#             return Response(data=serializer.data)
#         else:
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def get(self, request):
#         student = Student.objects.filter(user__is_student=True).order_by('-id')
#         group = Group.objects.all().order_by('-id')
#         serializer_student = StudentSerializer(student, many=True)
#         serializer_group = GroupSerializer(group, many=True)
#         data = {
#             "students": serializer_student.data,
#             "groups": serializer_group.data,
#         }
#         return Response(data=data)

class StudentApiView(APIView):
    @swagger_auto_schema(request_body=StudentSerializer)
    def post(self, request):
        serializer = StudentSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            phone = serializer.validated_data.get("phone")

            #  User yaratish yoki mavjudini olish
            user, created = User.objects.get_or_create(phone=phone, defaults={"is_student": True})

            if not created:
                user.is_student = True
                user.save()

            #  Student yaratish
            student = serializer.save(user=user)  # user qo‘shildi!

            return Response(StudentSerializer(student).data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class StudentApiViewId(APIView):
    pagination_class = CustomPagination
    def get(self, request, pk):
        try:
            student = Student.objects.get(pk=pk)
            serializer = StudentSerializer(student)
            return Response(data=serializer.data)
        except Exception as e:
            return Response(data={'error': e})

    def put(self, request, pk):
        try:
            student = Student.objects.get(id=pk)
            serializer = StudentSerializer(student, data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(data=serializer.data)
        except Exception as e:
            return Response(data={'error': e})

    def patch(self, request, pk):
        try:
            student = Student.objects.get(pk=pk)
            serializer = StudentSerializer(student, data=request.data, partial=True)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
                return Response(data=serializer.data)
        except Exception as e:
            return Response(data={'error': e})



class GroupApiView(ModelViewSet):
    pagination_class = CustomPagination
    queryset = Group.objects.all().order_by('-id')
    serializer_class = GroupSerializer



class GroupApi(APIView):
    pagination_class = CustomPagination

    def get(self, request):
        teachers = Worker.objects.filter(user__is_teacher=True).order_by('-id')
        tables = Table.objects.all().order_by('-id')
        serializer_teachers = WorkerSerializer(teachers, many=True)
        serializer_table = TableSerializer(tables, many=True)

        datas = {
            "teachers": serializer_teachers.data,
            "tables": serializer_table.data
        }

        return Response(data=datas)


# Guruh ichidagi studentlarni olish
class GroupStudentsView(APIView):
    def get(self, request, group_id):
        try:
            group = Group.objects.get(id=group_id)
            students = group.student.all()
            serializer = StudentSerializer(students, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Group.DoesNotExist:
            return Response({"error": "Group not found"}, status=status.HTTP_404_NOT_FOUND)


class TableTypeApi(ModelViewSet):
    pagination_class = CustomPagination
    queryset = TableType.objects.all().order_by('-id')
    serializer_class = TableTypeSerializer


class TableApi(ModelViewSet):
    pagination_class = CustomPagination
    queryset = Table.objects.all().order_by('-id')
    serializer_class = TableSerializer


class AttendanceLevelApi(ModelViewSet):
    queryset = AttendanceLevel.objects.all().order_by('-id')
    serializer_class = AttendanceLevelSerializer
    pagination_class = CustomPagination


class CourseApi(APIView):
    pagination_class = CustomPagination
    def get(self, request, pk=None):
        if pk:
            try:
                course = Course.objects.get(pk=pk)
                serializer = CourseSerializer(course)
                return Response(serializer.data, status=status.HTTP_200_OK)
            except Course.DoesNotExist:
                return Response({"error": "Course not found"}, status=status.HTTP_404_NOT_FOUND)
        else:
            courses = Course.objects.all()
            serializer = CourseSerializer(courses, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)


    @swagger_auto_schema(request_body=CourseSerializer)
    def post(self, request):
        """Yangi kurs qo'shish."""
        serializer = CourseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        try:
            course = Course.objects.get(pk=pk)
        except Course.DoesNotExist:
            return Response({"error": "Course not found"}, status=status.HTTP_404_NOT_FOUND)

        serializer = CourseSerializer(course, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            course = Course.objects.get(pk=pk)
            course.delete()
            return Response({"message": "Course deleted"}, status=status.HTTP_204_NO_CONTENT)
        except Course.DoesNotExist:
            return Response({"error": "Course not found"}, status=status.HTTP_404_NOT_FOUND)



class CourseApiView(ModelViewSet):
    queryset = Course.objects.all().order_by('-id')
    serializer_class = CourseSerializer
    pagination_class = CustomPagination


class StudentCreateAPIView(APIView):
    def post(self, request):
        serializer = StudentSerializer(data=request.data)

        if serializer.is_valid():
            phone = serializer.validated_data.get("phone")

            # Foydalanuvchini yaratish yoki mavjudini olish
            user, created = User.objects.get_or_create(phone=phone, defaults={"is_student": True})
            if not created:
                user.is_student = True
                user.save()

            # Student yaratish
            student = serializer.save(user=user)
            return Response(StudentSerializer(student).data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class StudentStatisticsView(APIView):
    def get(self, request):
        # Statistik ma’lumotlarni yig‘ish
        course_statistics = []
        courses = Course.objects.all()
        for course in courses:
            students = Student.objects.filter(course=course)

            statistics = {
                "course_name": course.name,
                "registered_students": students.count(),
                "active_students": students.filter(is_active=True).count(),
                "graduated_students": students.filter(is_graduated=True).count(),
            }
            course_statistics.append(statistics)

        return Response(course_statistics, status=status.HTTP_200_OK)


    def get_user_by_fullname_and_phone(full_name, phone):
        user = User.objects.filter(full_name=full_name, phone=phone).first()
        if user is None:
            return Response({"error": "Bunday foydalanuvchi topilmadi"}, status=status.HTTP_404_NOT_FOUND)
        return user



class StudentDetailView(APIView):
    def get(self, request, student_id):
        try:
            student = Student.objects.get(id=student_id)
            serializer = StudentSerializer(student)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Student.DoesNotExist:
            return Response({"error": "Student topilmadi."}, status=status.HTTP_404_NOT_FOUND)


class GroupDetailView(APIView):
    def get(self, request, group_id):
        try:
            group = Group.objects.get(id=group_id)
            serializer = GroupSerializer(group)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Group.DoesNotExist:
            return Response({"error": "Group topilmadi."}, status=status.HTTP_404_NOT_FOUND)



class StudentListView(ListAPIView):
    queryset = Student.objects.all().order_by('-id')
    serializer_class = StudentSerializer
    pagination_class = CustomPagination




