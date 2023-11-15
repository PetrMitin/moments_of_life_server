from django.http import JsonResponse, HttpResponseNotFound
from insta.models import Moment, Profile, MomentLike, CommentLike, Subscription
from insta.serializers import MomentSerializer, ProfileSerializer, MomentLikeEventSerializer, CommentLikeEventSerializer, SubscriptionEventSerializer
from django.core.paginator import Paginator, InvalidPage, PageNotAnInteger, EmptyPage, Page

def paginate(objects, page=1, per_page=45):
    try:
        paginator = Paginator(objects, per_page)
        return paginator.page(page)
    except InvalidPage or PageNotAnInteger or EmptyPage:
        return Page([], 0, paginator)

# Create your views here.
def moments_of_user_subscriptions(request):
    user_id = 31328
    page = request.GET.get('page')
    page = page if page else 1
    if request.user.is_authenticated:
        user_id = request.user.id
    curr_user_subscriptions = Subscription.objects.user_subscribed_to_ids(user_id=user_id).values('author_id')
    moments = Moment.objects.moments_by_user_subscriptions(curr_user_id=user_id, curr_user_subscriptions=curr_user_subscriptions)
    serializer = MomentSerializer(moments, many=True)
    data = paginate(serializer.data, page).object_list
    return JsonResponse(data, safe=False)

def moments_of_profile(request, profile_pk):
    curr_user_id = 31328
    if request.user.is_authenticated:
        curr_user_id = request.user.id
    moments = Moment.objects.moments_by_profile_id(curr_user_id=curr_user_id, profile_id=profile_pk)
    serializer = MomentSerializer(moments, many=True)
    return JsonResponse(serializer.data, safe=False)

def events_of_user(request):
    user_id = 31328
    if request.user.is_authenticated:
        user_id = request.user.id

    moment_likes = MomentLike.objects.by_moment_author_user(user_id=user_id)
    moment_likes_serializer = MomentLikeEventSerializer(moment_likes, many=True)

    comment_likes = CommentLike.objects.by_comment_author_user(user_id=user_id)
    comment_like_serializer = CommentLikeEventSerializer(comment_likes, many=True)

    subs = Subscription.objects.by_subscribed_to_user(user_id=user_id)
    sub_serializer = SubscriptionEventSerializer(subs, many=True)

    return JsonResponse({
            'moment_like_events': moment_likes_serializer.data,
            'comment_like_events': comment_like_serializer.data,
            'subscription_events': sub_serializer.data
        }, safe=False)

def profile_data(request, profile_pk):
    profile = Profile.objects.profile_by_id(profile_id=profile_pk)
    if not profile:
        return HttpResponseNotFound()
    serializer = ProfileSerializer(profile)
    return JsonResponse(serializer.data, safe=False)

def profiles_by_username(request, username):
    profiles = Profile.objects.profiles_by_username(username=username)
    serializer = ProfileSerializer(profiles, many=True)
    return JsonResponse(serializer.data, safe=False)

def moments_by_tag(request, tag):
    moments = Moment.objects.search_by_tag(tag=tag)
    serializer = MomentSerializer(moments, many=True)
    return JsonResponse(serializer.data, safe=False)