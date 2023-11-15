from rest_framework import serializers
from django.db import models
from insta.models import Profile, Moment, Comment, MomentLike, CommentLike, Subscription

class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ['id', 'number_of_moments', 'number_of_subscribers', 'number_of_subscriptions', 'rating', 'user']
        depth = 1

class CommentSerializer(serializers.ModelSerializer):
    is_liked = serializers.BooleanField()
    author = ProfileSerializer()
    
    class Meta:
        model = Comment
        fields = ['id', 'content', 'author', 'creation_date', 'moment', 'is_liked']

class MomentSerializer(serializers.ModelSerializer):
    is_liked = serializers.BooleanField(default=False)

    class Meta:
        model = Moment
        fields = ['id', 'content', 'author', 'creation_date', 'image', 'is_liked', 'comments']
        depth = 2

class MomentLikeEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = MomentLike
        fields = ['id', 'creation_date', 'author', 'moment']
        depth = 2

class CommentLikeEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentLike
        fields = ['id', 'creation_date', 'author', 'comment']
        depth = 2

class SubscriptionEventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subscription
        fields = ['id', 'subscription_date', 'author', 'subscriber']
        depth = 2
