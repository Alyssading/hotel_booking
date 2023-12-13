"""hotel_booking_sys URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from app import views

urlpatterns = [path('login/', views.user_login, name='login'),  # login
               path('logout/', views.user_logout, name='logout'),  # logout
               path('user_info/', views.user_info, name='user_info'),  # User modifies basic information
               path('change_pwd/', views.change_pwd, name='change_pwd'),  # User modifies password
               path('user_register/', views.user_register, name='user_register'),  # Registered user

               path('', views.index, name='index'),  # search page
               path('hotel_list/', views.hotel_list, name='hotel_list'),  # Search hotel list page

               ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
