from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from insta.managers import CommentManager, MomentLikeManager, MomentManager, ProfileManager, CommentLikeManager, SubscriptionManager
from django.db.models.signals import pre_delete, post_save
from django.dispatch import receiver

# Create your models here.

# Пользователь – электронная почта, никнейм, пароль, аватарка, дата регистрации, рейтинг.
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    avatar = models.ImageField(null=True)
    registration_date = models.DateTimeField(auto_now_add=True)
    subscriptions = models.ManyToManyField('Profile', through='Subscription', symmetrical=False)
    rating = models.BigIntegerField(default=0)
    number_of_moments = models.BigIntegerField(default=0)
    number_of_subscribers = models.BigIntegerField(default=0)
    number_of_subscriptions = models.BigIntegerField(default=0)

    objects = ProfileManager()

    def __str__(self):
        return self.user.username

# Момент – заголовок, содержание, автор, дата создания, изображение.
class Moment(models.Model):
    title = models.CharField(max_length=255)
    content = models.TextField()
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='moments')
    creation_date = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(null=True)

    objects = MomentManager()

@receiver(post_save, sender=Moment, dispatch_uid='moment_create_signal')
def increment_user_moments(sender, instance, using, **kwargs):
    Profile.objects.filter(id=instance.author_id).update(number_of_moments=models.F('number_of_moments') + 1)
        
@receiver(pre_delete, sender=Moment, dispatch_uid='moment_delete_signal')
def decrement_user_moments(sender, instance, using, **kwargs):
    Profile.objects.filter(id=instance.author_id).update(number_of_moments=models.F('number_of_moments') - 1)

# Комментарий – содержание, автор, дата написания
class Comment(models.Model): 
    content = models.TextField()
    author = models.ForeignKey(Profile, on_delete=models.CASCADE)
    moment = models.ForeignKey(Moment, on_delete=models.CASCADE, related_name='comments')
    creation_date = models.DateTimeField(auto_now_add=True)

    objects = CommentManager()

# Подписка - автор, подписчик, дата подписки
class Subscription(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='subscribed_to')
    subscriber = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='subscriber')
    subscription_date = models.DateTimeField(auto_now_add=True)

    objects = SubscriptionManager()

    class Meta:
        unique_together = ('author', 'subscriber')

@receiver(post_save, sender=Subscription, dispatch_uid='subscription_create_signal')
def increment_user_subs(sender, instance, using, **kwargs):
    Profile.objects.filter(id=instance.author_id).update(number_of_subscribers=models.F('number_of_subscribers') + 1)
    Profile.objects.filter(id=instance.subscriber_id).update(number_of_subscriptions=models.F('number_of_subscriptions') + 1)

@receiver(pre_delete, sender=Subscription, dispatch_uid='subscription_delete_signal')
def decrement_user_subs(sender, instance, using, **kwargs):
    Profile.objects.filter(id=instance.author_id).update(number_of_subscribers=models.F('number_of_subscribers') - 1)
    Profile.objects.filter(id=instance.subscriber_id).update(number_of_subscriptions=models.F('number_of_subscriptions') - 1)

# Лайк - автор, момент/комментарий, дата создания
class MomentLike(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='moment_likes_by')
    moment = models.ForeignKey(Moment, on_delete=models.CASCADE, related_name='moment_likes')
    creation_date = models.DateTimeField(auto_now_add=True)

    objects = MomentLikeManager()

    class Meta:
        unique_together = ('author', 'moment')     
        
class CommentLike(models.Model):
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='comment_likes_by')
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='comment_likes')
    creation_date = models.DateTimeField(auto_now_add=True)

    objects = CommentLikeManager()

    class Meta:
        unique_together = ('author', 'comment')        
        
@receiver(post_save, sender=MomentLike, dispatch_uid='moment_like_create_signal')
@receiver(post_save, sender=CommentLike, dispatch_uid='comment_like_create_signal')
def increment_user_rating(sender, instance, using, **kwargs):
    author_id = instance.comment.author_id if hasattr(instance, 'comment') else instance.moment.author_id
    Profile.objects.filter(id=author_id).update(rating=models.F('rating') + 1)
        
@receiver(pre_delete, sender=MomentLike, dispatch_uid='moment_like_delete_signal')
@receiver(pre_delete, sender=CommentLike, dispatch_uid='comment_like_delete_signal')
def decrement_user_rating(sender, instance, using, **kwargs):
    author_id = instance.comment.author_id if hasattr(instance, 'comment') else instance.moment.author_id
    Profile.objects.filter(id=author_id).update(rating=models.F('rating') - 1)

# Теги - момент, название
class Tag(models.Model):
    tag = models.CharField(max_length=255)
    moment = models.ForeignKey(Moment, on_delete=models.CASCADE)
