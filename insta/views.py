import json
from django.http import JsonResponse, HttpResponseNotFound, HttpResponseBadRequest
from django.views.decorators.http import require_GET
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from insta.models import *
from insta.serializers import *
from django.core.paginator import Paginator, InvalidPage, PageNotAnInteger, EmptyPage, Page
from insta.validators import *

def paginate(objects, page=1, per_page=45):
    try:
        paginator = Paginator(objects, per_page)
        return paginator.page(page)
    except InvalidPage or PageNotAnInteger or EmptyPage:
        return Page([], 0, paginator)

# Create your views here.
@require_GET
def moments_of_user_subscriptions(request):
    user_id = 31328
    page = request.GET.get('page')
    page = page if page else 1
    if request.user.is_authenticated:
        user_id = request.user.id
    curr_user_subscriptions = Subscription.objects.user_subscribed_to_ids(user_id=user_id).values('author_id')
    moments = Moment.objects.moments_by_user_subscriptions(curr_user_id=user_id, curr_user_subscriptions=curr_user_subscriptions)
    data = paginate(moments, page).object_list
    serializer = MomentSerializer(data, many=True)
    return JsonResponse(serializer.data, safe=False)

@require_GET
def moments_of_profile(request, profile_pk):
    curr_user_id = 31328
    if request.user.is_authenticated:
        curr_user_id = request.user.id
    moments = Moment.objects.moments_by_profile_id(curr_user_id=curr_user_id, profile_id=profile_pk)
    serializer = MomentSerializer(moments, many=True)
    return JsonResponse(serializer.data, safe=False)

@require_GET
def events_of_user(request):
    user_id = 31328
    page = request.GET.get('page')
    page = page if page else 1
    if request.user.is_authenticated:
        user_id = request.user.id

    moment_likes = MomentLike.objects.by_moment_author_user(user_id=user_id)
    moment_likes_data = paginate(moment_likes, page, 15).object_list
    moment_likes_serializer = MomentLikeEventSerializer(moment_likes_data, many=True)

    comment_likes = CommentLike.objects.by_comment_author_user(user_id=user_id)
    comment_likes_data = paginate(comment_likes, page, 15).object_list
    comment_like_serializer = CommentLikeEventSerializer(comment_likes_data, many=True)

    subs = Subscription.objects.by_subscribed_to_user(user_id=user_id)
    subs_data = paginate(subs, page, 15).object_list
    sub_serializer = SubscriptionEventSerializer(subs_data, many=True)

    return JsonResponse({
            'moment_like_events': moment_likes_serializer.data,
            'comment_like_events': comment_like_serializer.data,
            'subscription_events': sub_serializer.data
        }, safe=False)

@require_GET
def profile_data(request, profile_pk):
    profile = Profile.objects.profile_by_id(profile_id=profile_pk)
    if not profile:
        return HttpResponseNotFound()
    serializer = ProfileSerializer(profile)
    return JsonResponse(serializer.data, safe=False)

@require_GET
def profiles_by_username(request, username):
    profiles = Profile.objects.profiles_by_username(username=username)
    serializer = ProfileSerializer(profiles, many=True)
    return JsonResponse(serializer.data, safe=False)

@require_GET
def moments_by_tag(request, tag):
    moments = Moment.objects.search_by_tag(tag=tag)
    serializer = MomentSerializer(moments, many=True)
    return JsonResponse(serializer.data, safe=False)

@csrf_exempt
@api_view(['POST'])
def create_moment(request):
    title = request.data.get("title")
    content = request.data.get("content")
    profile = request.data.get("author")
    image = request.data.get("image")
    profile_data = json.loads(profile)
    if not is_moment_creation_data_valid(title, content, profile_data, image):
        return HttpResponseBadRequest()
    new_moment = Moment.objects.create_moment(title, content, profile_data, image)
    serializer = MomentSerializer(new_moment)
    return JsonResponse(serializer.data, safe=False)

@csrf_exempt
@api_view(['POST'])
def create_comment(request):
    content = request.data.get('content')
    profile_data = request.data.get('author')
    moment_id = request.data.get('moment_id')
    print(content, profile_data, moment_id)
    if not is_comment_creation_data_valid(content, profile_data, moment_id):
        return HttpResponseBadRequest()
    new_comment = Comment.objects.create_comment(content, profile_data, moment_id)
    serializer = CommentSerializer(new_comment)
    return JsonResponse(serializer.data, safe=False)

@csrf_exempt
@api_view(['POST'])
def create_moment_like(request):
    return JsonResponse({})

@csrf_exempt
@api_view(['POST'])
def create_comment_like(request):
    return JsonResponse({})

@csrf_exempt
@api_view(['POST'])
def create_subscription(request):
    return JsonResponse({})