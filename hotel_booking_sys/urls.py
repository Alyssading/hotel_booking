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
               path('hotel_search_detail/', views.hotel_search_detail, name='hotel_search_detail'),  # Search hotel details page

               path('booking_order/', views.booking_room, name='booking_order'),  # Hotel reservation form page
               path('booking_list/', views.booking_list, name='booking_list'),  # reservation list for user
               path('booking_manage_list/', views.booking_manage_list, name='booking_manage_list'),# reservation list for admin
               path('booking_detail/<int:id>', views.booking_detail, name='booking_detail'),  # reservation detail
               path('booking_cancel/<int:id>', views.booking_cancel, name='booking_cancel'),
               path('booking_status/<int:id>', views.booking_status, name='booking_status'),

               # Hotel Management
               path('hotel_manage_list/', views.hotel_manage_list, name='hotel_manage_list'),  # Hotel Management List
               path('hotel_manage_detail/', views.hotel_manage_detail, name='hotel_manage_add'),  # Hotel Management View: Add
               path('hotel_manage_detail/<int:id>', views.hotel_manage_detail, name='hotel_manage_detail'),  # Hotel Management View: Modifying
               # Hotel room type management
               path('room_manage_list/<int:hotel_id>', views.room_manage_list, name='room_manage_list'),  # Hotel Management List
               path('room_manage_detail/', views.room_manage_detail, name='room_manage_detail'),  # Hotel Management Details Page: Add
               path('room_manage_detail/<int:id>', views.room_manage_detail, name='room_manage_detail'),  # Hotel management details page: modification
               path('hotel_image/', views.hotel_image_view, name='hotel_image'),  # Hotel image main view: view, modify, add
               path('hotel_image_delete/<int:id>', views.hotel_image_delete, name='hotel_image_delete'),  # Delete image
               ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
