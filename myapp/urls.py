
# myapp/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('registration/', views.registration, name='registration'),
    path('dashboard_user/', views.dashboard, name='dashboard'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('message_show/', views.message_show, name='message_show'),
    path('logout/', views.logout, name='logout'),
]

