from django.urls import path, include
from .views import *

urlpatterns = [
    path('auth/login/', LoginApi.as_view(), name='token_obtain_pair'),

    path('users/create/', RegisterUserApi.as_view()),
    path('users/detail/<int:pk>/', UserDetailView.as_view(), name='users_detail'),
    path('users/teacher/create/', TeacherCreate.as_view(), name='teacher_create'),
    path('users/teacher/<int:pk>/', TeacherUpdate.as_view(), name='teacher_update'),
    path('users/student/create/', StudentCreate.as_view(), name='student_create'),
    path('users/student/<int:pk>/', StudentUpdateView.as_view(), name='student_update'),

    path('course/create/', CourseCreate.as_view(), name='course_create'),
    path('course/detail/<int:pk>/', CourseDetail.as_view(), name='course_detail'),
    path('course/group/create/', GroupCreate.as_view(), name='group_create'),
    path('course/group/<int:pk>/', GroupDetail.as_view(), name='group_detail'),
    path('course/table/create/', TableCreate.as_view(), name='table_create'),
    path('course/table/<int:pk>/', TableDetail.as_view(), name='table_detail'),
    path('course/table-type/create/', TableTypeCreate.as_view(), name='table_type_create'),
    path('course/table-type/<int:pk>/', TableTypeDetail.as_view(), name='table_type_detail'),
    path('course/rooms/create/', RoomsCreate.as_view(), name='rooms_create'),
    path('course/rooms/<int:pk>/', RoomsDetail.as_view(), name='rooms_detail'),
]