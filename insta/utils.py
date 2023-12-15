from django.contrib import auth
from insta.models import Profile
from insta.serializers import ProfileSerializer
from django.http import JsonResponse, HttpResponseBadRequest

def login_user(user, request):
    if user and request:
        password = request.data.get('password')
        user = auth.authenticate(username=user.username, password=password)
        if user:
            auth.login(request, user)
            profile = Profile.objects.profile_by_user_id(user.id)
            serializer = ProfileSerializer(profile, context={"request": request})
            return JsonResponse(serializer.data)
    return HttpResponseBadRequest()