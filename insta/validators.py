from insta.models import Profile, Moment, MomentLike, CommentLike, Subscription
from django.core.exceptions import ObjectDoesNotExist

# mb in serializer
def is_moment_creation_data_valid(title, content, profile, image):
    if not title or not content or not profile or not image:
        return False
    try:
        profile_id = profile['id']
        if not Profile.objects.filter(pk=profile_id).first():
            return False
    except KeyError:
        return False
    return True

# mb in serializer
def is_comment_creation_data_valid(content, profile, moment_id):
    if not content or not profile or not moment_id:
        return False
    try:
        profile_id = profile['id']
        if not Profile.objects.filter(pk=profile_id).first():
            return False
        if not Moment.objects.filter(pk=moment_id).first():
            return False
    except KeyError:
        return False
    return True

def is_moment_like_data_valid(moment_id, author_id):
    if not moment_id or not author_id:
        return False
    if MomentLike.objects.filter(moment_id=moment_id, author_id=author_id).first():
        return False
    return True

def is_comment_like_data_valid(comment_id, author_id):
    if not comment_id or not author_id:
        return False
    if CommentLike.objects.filter(comment_id=comment_id, author_id=author_id).first():
        return False
    return True

def is_subscription_like_data_valid(author_id, subscriber_id):
    if not subscriber_id or not author_id:
        return False
    if Subscription.objects.filter(subscriber_id=subscriber_id, author_id=author_id).first():
        return False
    return True

def is_delete_moment_like_data_valid(moment_id, author_id):
    if not moment_id or not author_id:
        return False
    if not MomentLike.objects.filter(moment_id=moment_id, author_id=author_id).first():
        return False
    return True

def is_delete_comment_like_data_valid(comment_id, author_id):
    if not comment_id or not author_id:
        return False
    if not CommentLike.objects.filter(comment_id=comment_id, author_id=author_id).first():
        return False
    return True

def is_delete_subscription_like_data_valid(author_id, subscriber_id):
    if not subscriber_id or not author_id:
        return False
    if not Subscription.objects.filter(subscriber_id=subscriber_id, author_id=author_id).first():
        return False
    return True