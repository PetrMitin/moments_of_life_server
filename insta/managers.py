from django.db import models
from django.db.models.functions import Coalesce

class ProfileManager(models.Manager):
    def with_stats(self):
        return self
    
    def profile_by_id(self, profile_id):
        return self.filter(id=profile_id).first()
    
    def profile_by_user_id(self, user_id):
        return self.filter(user=user_id).first()
    
    def subscribed_to(self, user_id):
        return self.profile_by_user_id(user_id=user_id).subscriptions.all()
    
    def is_subscribed_to_profile(self, user_id, profile_id):
        return self.subscribed_to(user_id=user_id).filter(subscrbed_to=profile_id).first()
    
    def profiles_by_username(self, username):
        return self.filter(user__username__contains=username)
    
class MomentManager(models.Manager):
    def moments_by_profile_id(self, curr_user_id, profile_id):
        return self.filter(author=profile_id).annotate(
                is_liked=models.Max(Coalesce(models.Case(models.When(momentlike__author__user=curr_user_id, then=1)), 0))
            )
    
    def moments_by_user_subscriptions(self, curr_user_id, curr_user_subscriptions):
        return (self
                .filter(author__in=curr_user_subscriptions)
                .order_by('creation_date')
                .annotate(
                is_liked=models.Max(Coalesce(models.Case(models.When(momentlike__author__user=curr_user_id, then=1)), 0))
            ))
    
    def search_by_tag(self, tag):
        return self.filter(tag__tag__contains=tag)
    
class CommentManager(models.Manager):
    def with_is_liked(self, curr_user_id):
        return self.annotate(is_liked=models.Max(Coalesce(models.Case(models.When(commentlike__author__user=curr_user_id, then=1)), 0)))

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