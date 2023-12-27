from insta.views import *
from django.urls import include, path

profile_urls = [
    path('<int:profile_pk>/', profile_data, name='profile_data'),
    path('<int:profile_pk>/update/', update_profile, name='update_profile'),
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
    path('like/', create_moment_like, name='like_moment'),
    path('unlike/', delete_moment_like, name='unlike_moment'),
]

comment_urls = [
    path('create/', create_comment, name='create_comment'),
    path('like/', create_comment_like, name='like_comment'),
    path('unlike/', delete_comment_like, name='unlike_comment'),
]

auth_urls = [
    path('get-csrf-token/', get_csrf_token, name='get_csrf_token'),
    path('registration/', registration, name='registration'),
    path('login/', login, name='login'),
    path('logout/', logout, name='logout'),
    path('is-authenticated/', is_authenticated, name='is_authenticated'),
    path('current-profile-data/', current_profile_data, name='current_profile_data'),
    path('get-centrifugo-token/', get_centrifugo_token, name='get_centrifugo_token')
]

urls = [
    path('profile/', include(profile_urls)),
    path('moments/', include(moment_urls)),
    path('comments/', include(comment_urls)),
    path('auth/', include(auth_urls)),
]
