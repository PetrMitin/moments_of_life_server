from insta.views import *
from django.urls import include, path

profile_urls = [
    path('<int:profile_pk>/', profile_data, name='profile_data'),
    path('<int:profile_pk>/moments/', moments_of_profile, name='moments_by_profile'),
    path('events/', events_of_user, name='events_by_profile'),
    path('search/', profiles_by_username, name='profiles_by_username'),
    path('subscribe/', create_subscription, name='subscribe'),
    path('unsubscribe/', delete_subscription, name='unsubscribe'),
]

moment_urls = [
    path('', moments_of_user_subscriptions, name='moments_by_subscriptions'),
    path('search/', moments_by_tag, name='moments_by_tag'),
    path('create/', create_moment, name='create_moment'),
    path('like', create_moment_like, name='like_moment'),
    path('unlike', delete_moment_like, name='unlike_moment'),
]

comment_urls = [
    path('create/', create_comment, name='create_comment'),
    path('like', create_comment_like, name='like_comment'),
    path('unlike', delete_comment_like, name='unlike_comment'),
]

urls = [
    path('profile/', include(profile_urls)),
    path('moments/', include(moment_urls)),
    path('comments/', include(comment_urls)),
]