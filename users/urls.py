from django.urls import path
from users import views

app_name = "users"


urlpatterns = [
    
    path('', views.index, name="index"),
    path('login/', views.login_view, name="login"),
    path('register/', views.register, name="register"),
    path('logout/', views.logout_view, name="logout"),
    path('track/<int:link_id>/', views.track_click, name="track_click"),
    path('<slug:slug>/', views.track_custom, name="track_custom"),
    path('delete/<int:link_id>/', views.delete_link, name='delete_link'),

  
    

]