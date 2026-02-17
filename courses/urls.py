from django.urls import path
from . import views

app_name = 'courses'   # обязательно

urlpatterns = [
    path('', views.index, name='index'),
    path('courses/', views.course_list, name='course_list'),
    path('course/<int:course_id>/', views.course_detail, name='course_detail'),
    path('course/<int:course_id>/lesson/<int:lesson_id>/', views.lesson_detail, name='lesson_detail'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('my-courses/', views.my_courses, name='my_courses'),

    #тесты
    path('course/<int:course_id>/tests/', views.test_list, name='test_list'),
    path('course/<int:course_id>/test/<int:test_id>/', views.test_detail, name='test_detail'),
    path('course/<int:course_id>/test/<int:test_id>/result/<int:attempt_id>/', views.test_result, name='test_result'),

    #экзамены
    path('course/<int:course_id>/exams/', views.exam_list, name='exam_list'),
    path('course/<int:course_id>/exam/<int:exam_id>/', views.exam_detail, name='exam_detail'),
    path('course/<int:course_id>/exam/<int:exam_id>/result/<int:attempt_id>/', views.exam_result, name='exam_result'),

]