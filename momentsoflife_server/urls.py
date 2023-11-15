"""
URL configuration for momentsoflife_server project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.contrib import admin
from django.urls import path
from insta import views

urlpatterns = [
    path('api/profile/<int:profile_pk>/', views.profile_data, name='profile_data'),
    path('api/profile/<int:profile_pk>/moments/', views.moments_of_profile, name='moments_by_profile'),
    path('api/events/', views.events_of_user, name='events_by_profile'),
    path('api/moments/', views.moments_of_user_subscriptions, name='moments_by_subscriptions'),
    path('api/moments/search/<str:tag>/', views.moments_by_tag, name='moments_by_tag'),
    path('api/profile/search/<str:username>', views.profiles_by_username, name='profiles_by_username'),
    path('api/admin/', admin.site.urls, name='admin'),
]
