from rest_framework import serializers
from django.db import models
from insta.models import *
from os.path import basename

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class ProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    avatar = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ['id', 'number_of_moments', 'number_of_subscribers', 'number_of_subscriptions', 'rating', 'user', 'avatar']
        depth = 1
    
    def get_avatar(self, obj):
        if obj.avatar:
            return basename(obj.avatar.name)
        return ''

class CommentSerializer(serializers.ModelSerializer):
    author = ProfileSerializer()
    is_liked = serializers.BooleanField(read_only=True)
    
    class Meta:
        model = Comment
        fields = ['id', 'content', 'author', 'creation_date', 'moment_id', 'is_liked']

class MomentSerializer(serializers.ModelSerializer):
    is_liked = serializers.BooleanField(read_only=True)
    comments = CommentSerializer(many=True)
    author = ProfileSerializer()
    image = serializers.SerializerMethodField()

    class Meta:
        model = Moment
        fields = ['id', 'content', 'author', 'creation_date', 'image', 'is_liked', 'comments']
    
    def get_image(self, obj):
        if obj.image:
            return basename(obj.image.name)
        return ''

class MomentLikeEventSerializer(serializers.ModelSerializer):
    author = ProfileSerializer()
    
    class Meta:
        model = MomentLike
        fields = ['id', 'creation_date', 'author', 'moment']
        depth = 2

class CommentLikeEventSerializer(serializers.ModelSerializer):
    author = ProfileSerializer()
    
    class Meta:
        model = CommentLike
        fields = ['id', 'creation_date', 'author', 'comment']
        depth = 2

class SubscriptionEventSerializer(serializers.ModelSerializer):
    subscriber = ProfileSerializer()
    author = ProfileSerializer()
    
    class Meta:
        model = Subscription
        fields = ['id', 'creation_date', 'author', 'subscriber']
        depth = 2
