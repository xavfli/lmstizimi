from django.urls import path, include
from .views import *
from rest_framework.routers import DefaultRouter


router = DefaultRouter()



router.register(r'department', DepartmentsApiView)
router.register(r'group', GroupApiView)
router.register(r'tableType', TableTypeApi)
router.register(r'table', TableApi)
router.register(r'attendanceLevel', AttendanceLevelApi)
# router.register(r'Course', CourseApi)
# router.register(r'teachergroup', TeacherGroupView)


urlpatterns = [
    path('', include(router.urls)),
    path('userApi/', RegisterUserApi.as_view()),
    path('refresh_password/', ChangePasswordView.as_view()),
    path('sentOTP/', PhoneSendOTP.as_view()),
    path('sentOTP_and_phone/', VerifySms.as_view()),
    path('teacherAPI/', TeacherApiView.as_view()),
    path('teacher-list/', TeacherListApiView.as_view(), name='teacher_list'),
    path('teacher-group/', TeacherGroupsView.as_view(), name='teacher_group'),
    path('workerAPI/', WorkerApiView.as_view()),
    path('workerId/<int:pk>/', WorkerApiViewId.as_view()),
    path('student/', StudentApiView.as_view()),
    path("groups/<int:group_id>/students/", GroupStudentsView.as_view(), name="group-students"),
    path('student/<int:pk>/', StudentApiView.as_view()),
    path('student_list/', StudentListView.as_view(), name='student_list'),
    path('group_get/', GroupApi.as_view()),
    # path('group/', GroupApiView.as_view(), name='group'),
    path('courses/', CourseApi.as_view()),
    path('courses/<int:pk>/', CourseApi.as_view()),
    path("student-statistics/", StudentStatisticsView.as_view(), name="student-statistics"),
    path('filter-student/<int:student_id>/', StudentDetailView.as_view(), name='filter-student'),
    path('filter-group/<int:group_id>/', GroupDetailView.as_view(), name='filter-group'),
    path('students-Pagination/', StudentListView.as_view(), name='student-pagination'),
]
