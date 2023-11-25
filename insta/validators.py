from insta.models import Profile, Moment
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