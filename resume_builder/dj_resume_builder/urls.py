from django.urls import path
from . import views

urlpatterns = [
    
  path('login/', views.loginUser, name="login"),
  path('logout/', views.logoutUser, name="logout"),
  path('register/', views.registerUser, name="register"),

  path('',views.info,name="info"),
  path('resume/',views.home,name="home"),
  path('generate_pdf/<int:pk>/',views.generatePdf,name="generate_pdf"),
  path('edit_resume/<int:pk>/',views.editResume,name='resume_edit'),
  path('resume_detail/<int:pk>/', views.resume_detail, name='resume_detail'),
  path('profile/<str:pk>/', views.user_profile, name='user_profile'),
   path('update-user/', views.updateUser, name="update-user"),

]
