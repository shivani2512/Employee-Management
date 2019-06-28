from django.urls import path
from . import views


app_name = 'emp'

urlpatterns = [
    path('register/', views.registration, name='register'),
    path('login/', views.login_user, name='login'),
    path('userlist/', views.UserList.as_view(), name='userlist'),
    path('emplist/', views.Emplist.as_view(), name='emplist'),
    path('detail/<int:pk>/', views.UserDetail.as_view(), name='detail'),
    path('update/<int:pk>', views.UserUpdate.as_view(), name='update'),
    path('Addemp/<int:pk>', views.user_change_status, name='emp'),
    path('Deleteemp/<int:pk>', views.user_change_status, name='dltemp'),
    path('logout', views.logout_user, name='logout'),
]


