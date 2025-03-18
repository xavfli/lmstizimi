from rest_framework import serializers
from app_users.models import *


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Course
        fields = '__all__'


class CourseStatisticsSerializer(serializers.Serializer):
    course_name = serializers.CharField()
    registered_students = serializers.IntegerField()
    active_students = serializers.IntegerField()
    graduated_students = serializers.IntegerField()



class ChangePasswordSerializer(serializers.ModelSerializer):
    old_password = serializers.CharField(required=True, write_only=True)
    new_password = serializers.CharField(required=True, write_only=True)
    re_new_password = serializers.CharField(required=True, write_only=True)

    def update(self, instance, validated_data):

        instance.password = validated_data.get('password', instance.password)

        if not validated_data['new_password']:
            raise serializers.ValidationError({'new_password': 'not found'})

        if not validated_data['old_password']:
            raise serializers.ValidationError({'old_password': 'not found'})

        if not instance.check_password(validated_data['old_password']):
            raise serializers.ValidationError({'old_password': 'wrong password'})

        if validated_data['new_password'] != validated_data['re_new_password']:
            raise serializers.ValidationError({'passwords': 'passwords do not match'})

        if validated_data['new_password'] == validated_data['re_new_password'] and instance.check_password(
                validated_data['old_password']):
            instance.set_password(validated_data['new_password'])
            instance.save()
            return instance

    class Meta:
        model = User
        fields = ['old_password', 'new_password', 're_new_password']


class SMSSerializer(serializers.Serializer):
    phone_number = serializers.CharField()

    class Meta:
        model = User
        fields = '__all__'


class VerifySMSSerializer(serializers.Serializer):
    phone_number = serializers.CharField()
    verification_code = serializers.CharField()



class DepartmentsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Departments
        fields = ['id', 'title', 'is_active', 'descriptions']



class WorkerSerializer(serializers.ModelSerializer):
    phone = serializers.CharField(write_only=True)  # Faqat yozish uchun
    full_name = serializers.CharField(write_only=True)  # Faqat yozish uchun
    # user = UserSerializer(read_only=True)  # O‘qish uchun (user obyektini ko‘rsatish)

    class Meta:
        model = Worker
        fields = ['phone', 'full_name', 'course', 'departments', 'descriptions']

    def create(self, validated_data):
        departments_data = validated_data.pop("departments", [])
        worker = Worker.objects.create(**validated_data)
        worker.departments.set(departments_data)
        return worker


class GroupSerializer(serializers.ModelSerializer):
    # teacher = TeacherSerializer(many=True, read_only=True)
    # table = TableSerializer(read_only=True)

    class Meta:
        model = Group
        fields = ['id', 'name', 'title', 'course', 'teacher', 'table', 'created', 'updated', 'price', 'descriptions']




class TableTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TableType
        fields = ['id', 'title', 'descriptions']



class TableSerializer(serializers.ModelSerializer):
    class Meta:
        model = Table
        fields = ['id', 'type', 'descriptions']



class StudentSerializer(serializers.ModelSerializer):
    # user = serializers.PrimaryKeyRelatedField(
    #     queryset=User.objects.all(), required=False
    # )

    class Meta:
        model = Student
        fields = [
            "phone",
            "is_line",
            "course",
            "group",
            "descriptions",
            "is_active",
            "is_graduated",
        ]



class AttendanceLevelSerializer(serializers.ModelSerializer):

    class Meta:
        model = Attendance
        fields = "__all__"



class TeacherSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    full_name = serializers.CharField(write_only=True)

    class Meta:
        model = Teacher
        fields = ["full_name", "phone", "course", "departments", "descriptions"]


    def get_full_name(self, obj):
        return f"{obj.first_name} {obj.last_name}"



class TeacherGroupSerializer(serializers.Serializer):
    teacher = TeacherSerializer(many=True)
    group = GroupSerializer(many=True)



# class TeacherGroupSerializer(serializers.Serializer):
#     full_name = serializers.CharField()
#     phone = serializers.CharField()
#     group = serializers.PrimaryKeyRelatedField(queryset=Group.objects.all(), many=True)
#
#     def validate(self, data):
#         full_name = data.get("full_name")
#         phone = data.get("phone")
#
#         try:
#             user = User.objects.get(full_name=full_name, phone=phone, is_teacher=True)
#         except User.DoesNotExist:
#             raise serializers.ValidationError("Foydalanuvchi topilmadi yoki u teacher emas!")
#
#         try:
#             teacher = Teacher.objects.get(user=user)
#         except Teacher.DoesNotExist:
#             raise serializers.ValidationError("Teacher topilmadi!")
#
#         data["teacher"] = teacher
#         return data
#
#     def create(self, validated_data):
#         teacher = validated_data["teacher"]
#         groups = validated_data["group"]
#         teacher.groups.set(groups)
#         return {"teacher": teacher.name, "group": [g.name for g in groups]}



class UserAndStudentSerializer(serializers.Serializer):
    user = UserSerializer()
    student = StudentSerializer()


class CommitSerializer(serializers.ModelSerializer):
    class Meta:
        model = Commit
        fields = '__all__'



class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = '__all__'
        read_only_fields = ['status', 'created_at']




