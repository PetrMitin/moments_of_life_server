from insta.views import *
from django.urls import path

urls = [
    path('profile/<int:profile_pk>/', profile_data, name='profile_data'),
    path('profile/<int:profile_pk>/moments/', moments_of_profile, name='moments_by_profile'),
    path('events/', events_of_user, name='events_by_profile'),
    path('moments/', moments_of_user_subscriptions, name='moments_by_subscriptions'),
    path('moments/search/<str:tag>/', moments_by_tag, name='moments_by_tag'),
    path('profile/search/<str:username>', profiles_by_username, name='profiles_by_username'),
    path('moments/create', create_moment, name='create_moment'),
    path('comments/create', create_comment, name='create_comment'),
]