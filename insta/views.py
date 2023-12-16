import json
from django.http import JsonResponse, HttpResponseNotFound, HttpResponseBadRequest
from django.views.decorators.http import require_GET
from django.views.decorators.csrf import csrf_exempt, ensure_csrf_cookie, csrf_protect
from django.contrib import auth
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import SessionAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny
from insta.models import *
from insta.serializers import *
from django.core.paginator import Paginator, InvalidPage, PageNotAnInteger, EmptyPage, Page
from insta.validators import *
from django.db.models.functions import Coalesce
from django.contrib.auth.hashers import make_password
from insta.utils import login_user

def paginate(objects, page=1, per_page=45):
    try:
        paginator = Paginator(objects, per_page)
        return paginator.page(page)
    except InvalidPage or PageNotAnInteger or EmptyPage:
        return Page([], 0, paginator)

# Create your views here.
@api_view(['GET'])
def moments_of_user_subscriptions(request):
    page = request.GET.get('page')
    page = page if page else 1
    user_id = request.user.id
    curr_profile = Profile.objects.profile_by_user_id(user_id)
    if not curr_profile:
        return HttpResponseBadRequest()
    curr_profile_id = curr_profile.id
    curr_user_subscriptions = Subscription.objects.user_subscribed_to_ids(user_id=user_id).values('author_id')
    moments = Moment.objects.moments_by_user_subscriptions(
        curr_profile_id=curr_profile_id, 
        curr_user_subscriptions=curr_user_subscriptions
    ).order_by('-creation_date')
    data = paginate(moments, page).object_list
    serializer = MomentSerializer(data, many=True, context={"request": request})
    return JsonResponse(serializer.data, safe=False)

@api_view(['GET'])
def moments_of_profile(request, profile_pk):
    curr_user_id = request.user.id
    curr_profile_id = Profile.objects.profile_by_user_id(curr_user_id).id
    profile = Profile.objects.filter(id=profile_pk).first()
    if not (curr_profile_id and profile):
        return HttpResponseBadRequest()
    moments = Moment.objects.moments_by_profile_id(curr_profile_id=curr_profile_id, profile_id=profile_pk)
    serializer = MomentSerializer(moments, many=True, context={"request": request})
    return JsonResponse(serializer.data, safe=False)

@api_view(['GET'])
def events_of_user(request):
    page = request.GET.get('page')
    page = page if page else 1
    user_id = request.user.id

    moment_likes = MomentLike.objects.by_moment_author_user(user_id=user_id).order_by('-creation_date')
    moment_likes_data = paginate(moment_likes, page, 15).object_list
    moment_likes_serializer = MomentLikeEventSerializer(moment_likes_data, many=True)

    comment_likes = CommentLike.objects.by_comment_author_user(user_id=user_id).order_by('-creation_date')
    comment_likes_data = paginate(comment_likes, page, 15).object_list
    comment_like_serializer = CommentLikeEventSerializer(comment_likes_data, many=True)

    subs = Subscription.objects.by_subscribed_to_user(user_id=user_id).order_by('-subscription_date')
    subs_data = paginate(subs, page, 15).object_list
    sub_serializer = SubscriptionEventSerializer(subs_data, many=True)

    return JsonResponse({
            'moment_like_events': moment_likes_serializer.data,
            'comment_like_events': comment_like_serializer.data,
            'subscription_events': sub_serializer.data
        }, safe=False)

@api_view(['GET'])
def profile_data(request, profile_pk):
    user_id = request.user.id
    profile = Profile.objects.profile_by_id(profile_id=profile_pk)
    if not profile:
        return HttpResponseNotFound()
    is_subscribed_flag = bool(Profile.objects.is_subscribed_to_profile(user_id=user_id, profile_id=profile.id))
    serializer = ProfileSerializer(profile, context={"request": request})
    return JsonResponse({'profile': serializer.data, 'is_subscribed_flag': is_subscribed_flag}, safe=False)

@api_view(['PUT'])
@csrf_protect
def update_profile(request, profile_pk):
    profile = Profile.objects.profile_by_id(profile_id=profile_pk)
    user = User.objects.filter(id=profile.user_id).first()
    if not profile or not user:
        return HttpResponseNotFound()
    email = request.data.get('email')
    username = request.data.get('username')
    password = request.data.get('password')
    avatar = request.data.get('avatar')
    if not is_update_profile_data_valid(email, username, password, avatar):
        return HttpResponseBadRequest()
    if avatar:
        profile.avatar = avatar
    profile.save()
    if username:
        user.username = username
    if email:
        user.email = email
    if password:
        user.set_password(raw_password=password)
    user.save()
    serializer = ProfileSerializer(profile, context={"request": request})
    return JsonResponse(serializer.data)
    
@api_view(['GET'])
def profiles_by_username(request):
    username = request.GET.get('query')
    if not username:
        return HttpResponseBadRequest()
    profiles = Profile.objects.profiles_by_username(username=username)
    serializer = ProfileSerializer(profiles, many=True, context={"request": request})
    return JsonResponse(serializer.data, safe=False)

@api_view(['GET'])
def moments_by_tag(request):
    tag = request.GET.get('query')
    if not tag:
        return HttpResponseBadRequest()
    moments = Moment.objects.search_by_tag(tag=tag)
    serializer = MomentSerializer(moments, many=True, context={"request": request})
    return JsonResponse(serializer.data, safe=False)

@csrf_protect
@api_view(['POST'])
def create_moment(request):
    title = request.data.get("title")
    content = request.data.get("content")
    profile = request.data.get("author")
    image = request.data.get("image")
    if profile:
        profile_data = json.loads(profile)
    else:
        return HttpResponseBadRequest()
    if not is_moment_creation_data_valid(title, content, profile_data, image):
        return HttpResponseBadRequest()
    new_moment = Moment.objects.create_moment(title, content, profile_data, image)
    new_tags = [Tag(moment_id=new_moment.id, tag=tag) for tag in new_moment.content.split(' ') if tag[0] == '#']
    Tag.objects.bulk_create(new_tags)
    serializer = MomentSerializer(new_moment, context={"request": request})
    return JsonResponse(serializer.data, safe=False)

@csrf_protect
@api_view(['POST'])
def create_comment(request):
    content = request.data.get('content')
    profile_data = request.data.get('author')
    moment_id = request.data.get('moment_id')
    if not is_comment_creation_data_valid(content, profile_data, moment_id):
        return HttpResponseBadRequest()
    new_comment = Comment.objects.create_comment(content, profile_data, moment_id)
    serializer = CommentSerializer(new_comment)
    return JsonResponse(serializer.data, safe=False)

@csrf_protect
@api_view(['POST'])
def create_moment_like(request):
    moment_id = request.data.get('moment_id')
    author_id = request.data.get('author_id')
    if not is_moment_like_data_valid(moment_id, author_id):
        return HttpResponseBadRequest()
    moment_like = MomentLike.objects.create(moment_id=moment_id, author_id=author_id)
    serializer = MomentLikeEventSerializer(moment_like)
    return JsonResponse(serializer.data, safe=False)

@csrf_protect
@api_view(['DELETE'])
def delete_moment_like(request):
    moment_id = request.data.get('moment_id')
    author_id = request.data.get('author_id')
    if not is_delete_moment_like_data_valid(moment_id, author_id):
        return HttpResponseBadRequest()
    deletion_data = MomentLike.objects.filter(moment_id=moment_id, author_id=author_id).delete()
    return JsonResponse({'successful': deletion_data[0] > 0})

@csrf_protect
@api_view(['POST'])
def create_comment_like(request):
    comment_id = request.data.get('comment_id')
    author_id = request.data.get('author_id')
    if not is_comment_like_data_valid(comment_id, author_id):
        return HttpResponseBadRequest()
    comment_like = CommentLike.objects.create(comment_id=comment_id, author_id=author_id)
    serializer = CommentLikeEventSerializer(comment_like)
    return JsonResponse(serializer.data, safe=False)

@csrf_protect
@api_view(['DELETE'])
def delete_comment_like(request):
    comment_id = request.data.get('comment_id')
    author_id = request.data.get('author_id')
    if not is_delete_comment_like_data_valid(comment_id, author_id):
        return HttpResponseBadRequest()
    deletion_data = CommentLike.objects.filter(comment_id=comment_id, author_id=author_id).delete()
    return JsonResponse({'successful': deletion_data[0] > 0})

@csrf_protect
@api_view(['POST'])
def create_subscription(request):
    subscriber_id = request.data.get('subscriber_id')
    author_id = request.data.get('author_id')
    if not is_subscription_like_data_valid(author_id, subscriber_id):
        return HttpResponseBadRequest()
    sub = Subscription.objects.create(subscriber_id=subscriber_id, author_id=author_id)
    serializer = SubscriptionEventSerializer(sub)
    return JsonResponse(serializer.data, safe=False)

@csrf_protect
@api_view(['DELETE'])
def delete_subscription(request):
    subscriber_id = request.data.get('subscriber_id')
    author_id = request.data.get('author_id')
    if not is_delete_subscription_like_data_valid(author_id, subscriber_id):
        return HttpResponseBadRequest()
    deletion_data = Subscription.objects.filter(subscriber_id=subscriber_id, author_id=author_id).delete()
    return JsonResponse({'successful': deletion_data[0] > 0})

@ensure_csrf_cookie
@api_view(['GET'])
@permission_classes([AllowAny])
def get_csrf_token(request):
    return JsonResponse({'success': True})

@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_protect
def registration(request):
    email = request.data.get('email')
    username = request.data.get('username')
    password = request.data.get('password')
    avatar = request.data.get('avatar')
    if not is_registration_data_valid(email, username, password, avatar):
        return HttpResponseBadRequest()
    user = User(username=username, email=email)
    user.set_password(raw_password=password)
    user.save()
    if user and request:
        user = auth.authenticate(username=user.username, password=password)
        if user:
            auth.login(request, user)
            profile = Profile.objects.create(user=user, avatar=avatar)
            serializer = ProfileSerializer(profile, context={"request": request})
            return JsonResponse(serializer.data)
    return HttpResponseBadRequest()

@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_protect
def login(request):
    email = request.data.get('email')
    password = request.data.get('password')
    if not is_login_data_valid(email, password):
        return HttpResponseBadRequest()
    user = User.objects.filter(email=email).first()
    if user and request:
        user = auth.authenticate(username=user.username, password=password)
        if user:
            auth.login(request, user)
            profile = Profile.objects.profile_by_user_id(user.id)
            serializer = ProfileSerializer(profile, context={"request": request})
            return JsonResponse(serializer.data)
    return HttpResponseBadRequest()

@api_view(['POST'])
@csrf_protect
def logout(request):
    auth.logout(request)
    return JsonResponse({'success': True})
    
@api_view(['GET'])
@permission_classes([AllowAny])
def is_authenticated(request):
    res = False
    if request.user and request.user.is_authenticated:
        res = True
    return JsonResponse({'isAuthenticated': res})

@api_view(['GET'])
def current_profile_data(request):
    if request.user and request.user.is_authenticated:
        profile = Profile.objects.profile_by_user_id(user_id=request.user.id)
        if not profile:
            return HttpResponseNotFound()
        serializer = ProfileSerializer(profile, context={"request": request})
        return JsonResponse({serializer.data})
    return HttpResponseBadRequest()