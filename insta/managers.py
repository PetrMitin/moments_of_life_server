from django.db import models
from django.db.models.functions import Coalesce
from django.db.models import Q

class ProfileManager(models.Manager):
    def with_stats(self):
        return self
    
    def profile_by_id(self, profile_id):
        return self.filter(id=profile_id).first()
    
    def profile_by_user_id(self, user_id):
        return self.filter(user=user_id).first()
    
    def subscribed_to(self, user_id):
        return self.profile_by_user_id(user_id=user_id).subscriber.values('author_id').all()
    
    def is_subscribed_to_profile(self, user_id, profile_id):
        return self.subscribed_to(user_id=user_id).filter(author_id=profile_id).first()
    
    def profiles_by_username(self, username):
        return self.filter(user__username__contains=username)
    
class MomentManager(models.Manager):
    def moments_by_profile_id(self, curr_profile_id, profile_id):
        return self.filter(author=profile_id).annotate(
                    is_liked=models.Max(Coalesce(models.Case(models.When(moment_likes__author_id__exact=curr_profile_id, then=1)), 0))
            )
    
    def moments_by_user_subscriptions(self, curr_profile_id, curr_user_subscriptions):
        result = (self
                .filter(author__in=curr_user_subscriptions)
                .order_by('creation_date')
                .annotate(
                    is_liked=models.Max(Coalesce(models.Case(models.When(moment_likes__author_id__exact=curr_profile_id, then=1)), 0))
            ))
        return result
    
    def search_by_tag(self, tag):
        return self.filter(tag__tag__contains=tag)
    
    def create_moment(self, title, content, profile_data, image):
        new_moment = self.create(title=title, content=content, author_id=profile_data['id'], image=image)
        return new_moment
    
class CommentManager(models.Manager):
    def with_is_liked(self, curr_profile_id):
        return (self
                .annotate(
                    is_liked=models.Max(Coalesce(models.Case(models.When(comment_likes__author_id__exact=curr_profile_id, then=1)), 0))
                ))
    
    def create_comment(self, content, profile_data, moment_id):
        return self.create(content=content, author_id=profile_data['id'], moment_id=moment_id)

class MomentLikeManager(models.Manager):
    def by_moment_author_user(self, user_id):
        return self.filter(moment__author__user=user_id)
    
class CommentLikeManager(models.Manager):
    def by_comment_author_user(self, user_id):
        return self.filter(comment__author__user=user_id)

class SubscriptionManager(models.Manager):
    def by_subscribed_to_user(self, user_id):
        return self.filter(author__user=user_id)
    
    def user_subscribed_to_ids(self, user_id):
        return self.filter(subscriber__user=user_id).values('author_id')