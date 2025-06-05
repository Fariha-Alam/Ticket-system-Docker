
# myapp/urls.py
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.login_view, name='login'),
    path('registration/', views.registration, name='registration'),
    path('dashboard_user/', views.dashboard, name='dashboard'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),

    # urls.py
    path('tickets/<int:ticket_id>/messages/', views.message_show, name='message_show'),
    path('tickets/<int:ticket_id>/mark_solved/', views.mark_solved, name='mark_solved'),
 
    path('logout/', views.logout, name='logout'),
    path('update_ticket_status/<int:ticket_id>/', views.update_ticket_status, name='update_ticket_status'),
    path('export_tickets/', views.export_tickets_excel, name='export_tickets'),

]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)