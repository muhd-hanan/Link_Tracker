from django.urls import path
from . import views

app_name = "manager"

urlpatterns = [
   path('adminpanel/', views.adminpanel, name='adminpanel'),  
   path('logout/', views.manager_logout, name='logout'),
   path('delete-user/<int:user_id>/', views.delete_user, name='delete_user'),  # NEW

    path('delete-link/<int:link_id>/', views.delete_link, name='delete_link'),
    path('view-link/<int:link_id>/', views.view_link_details, name='view_link'),
]