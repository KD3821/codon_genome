from django.urls import path
from . import views

urlpatterns = [
    path('form/', views.form_view, name='check'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.register_view, name='register'),
]