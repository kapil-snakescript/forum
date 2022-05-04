from django import views
from django.urls import  path
from . import views



urlpatterns = [
      path('user',views.user_list, name='users-listing'),
      path('register/',views.register, name='register-user'),
      path('login/',views.login, name='login-user'),
      path('my-profile/',views.my_profile, name='my-profile'),
      path('logout/',views.logout, name='logout-user'),
      path('edit-profile/',views.edit_profile, name='edit-profile'),
      path('edit-user/<int:pk>/',views.edit_user,name="edit-user")
      
]