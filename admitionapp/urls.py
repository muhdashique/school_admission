from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.mobile_login, name='login'),
    path('forms/', views.forms, name='forms'),
    path('admission-form/', views.admission_form, name='admission_form'),
    path('request-otp/', views.request_otp, name='request_otp'),
    path('verify_otp_view/', views.verify_otp_view, name='verify_otp_view'),
    path('admin-panel/', views.admin_panel, name='admin_panel'),
    path('admin-login/', views.admin_login, name='admin_login'),
    path('admin-logout/', views.admin_logout, name='admin_logout'),
    path('edit-student/<int:student_id>/', views.edit_student, name='edit_student'),
    path('delete-student/<int:student_id>/', views.delete_student, name='delete_student'),
    path('edit-registered-student/<int:student_id>/', views.edit_registered_student, name='edit_registered_student'),
    path('student-delete/<int:student_id>/', views.student_delete, name='student_delete'),
    path('add-school-info/', views.add_school_info, name='add_school_info'),
]