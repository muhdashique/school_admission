from django.urls import path
from . import views  # Ensure this import is correct

urlpatterns = [
      path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('forms/', views.admission_form, name='admission_form'),
    path('request_otp/', views.request_otp, name='request_otp'),
    path('verify_otp/', views.verify_otp_view, name='verify_otp'),
    
    # Also add aliases with hyphens to handle both versions
    path('request-otp/', views.request_otp, name='request-otp'),
    path('verify-otp/', views.verify_otp_view, name='verify-otp'),
    path('admission/', views.admission_form, name='admission_form'),
    path('admission_form/', views.admission_form, name='admission_form'),
    path('admin-panel/', views.admin_panel, name='admin_panel'),
     path('admission/', views.admission_form, name='admission_form'),
      path('edit-student/<int:student_id>/', views.edit_student, name='edit_student'),  # ✅ Check URL name
    path('delete-student/<int:student_id>/', views.delete_student, name='delete_student'),
    path('student/edit/<int:student_id>/', views.edit_registered_student, name='edit_registered_student'),

   path('student/delete/<int:student_id>/', views.student_delete, name='student_delete'),

     path("admin-logout/", views.admin_logout, name="admin_logout"),
    
     


      

]
