from django.core.management import BaseCommand
import pytz
from django.db.models import F
from insta.models import User, Profile, Moment, Comment, Subscription, MomentLike, CommentLike, Tag
from random import randint
from datetime import datetime
from django.db.transaction import atomic

class Command(BaseCommand):
    help = """
                Fills database with fake data
                Пользователи > 10 000.
                Вопросы > 100 000.
                Ответы > 1 000 000.
                Тэги > 10 000.
                Оценки пользователей > 2 000 000.
            """

    def add_arguments(self, parser):
        parser.add_argument("num", type=int)

    @atomic
    def handle(self, *args, **kwargs):
        num = kwargs['num']
        users = []
        profiles = []
        profiles_update_data = [[0, 0, 0, 0] for i in range(num)]
        for i in range(num):
            user = User(username=f'Username{i}', email=f'email{i}@xmpl.com', password=f'password{i}', last_login=datetime.now(tz=pytz.UTC))
            users.append(user)
            profiles.append(Profile(user=user))
        User.objects.bulk_create(users)
        Profile.objects.bulk_create(profiles)
        print('Profiles created', datetime.now())

        moments = []
        for i in range(num * 10):
            author_id = randint(profiles[0].id, profiles[0].id + num - 1)
            author_idx = author_id - profiles[0].id
            moments.append(Moment(author_id=author_id, title=f'Title {i}', content=f'{i}. Lorem ipsum dolor sit amet cis team spirit 2 times TI winners'))
            profiles_update_data[author_idx][1] += 1
        Moment.objects.bulk_create(moments)
        print('Moments created', datetime.now())

        comments = [
            Comment(content=f'Comment content {i}', author_id=randint(profiles[0].id, profiles[0].id + num - 1), moment_id=randint(moments[0].id, moments[0].id + num * 10 - 1))
            for i in range(num * 100)
        ]
        Comment.objects.bulk_create(comments)
        print('Comments created', datetime.now())

        subs = []
        for i in range(num * 10):
            author_id = randint(profiles[0].id, profiles[0].id + num - 1)
            sub_id = randint(profiles[0].id, profiles[0].id + num - 1)
            author_idx = author_id - profiles[0].id
            sub_idx = sub_id - profiles[0].id
            subs.append(Subscription(author_id=author_id, subscriber_id=sub_id))
            profiles_update_data[author_idx][2] += 1
            profiles_update_data[sub_idx][3] += 1
        Subscription.objects.bulk_create(subs)
        print('Subs created', datetime.now())

        moment_likes = []
        for i in range(num * 100):
            author_id = randint(profiles[0].id, profiles[0].id + num - 1)
            moment_likes.append(MomentLike(author_id=author_id, moment_id=randint(moments[0].id, moments[0].id + num * 10 - 1)))
            author_idx = author_id - profiles[0].id
            profiles_update_data[author_idx][0] += 1
        MomentLike.objects.bulk_create(moment_likes)
        print('Moment likes created', datetime.now())

        comment_likes = []
        for i in range(num * 100):
            author_id = randint(profiles[0].id, profiles[0].id + num - 1)
            comment_likes.append(CommentLike(author_id=author_id, comment_id=randint(comments[0].id, comments[0].id + num * 100 - 1)))
            author_idx = author_id - profiles[0].id
            profiles_update_data[author_idx][0] += 1
        CommentLike.objects.bulk_create(comment_likes)
        print('Comment likes created', datetime.now())

        tags = [
            Tag(moment_id=randint(moments[0].id, moments[0].id + num * 10 - 1), tag=f'#tag{i}')
            for i in range(num)
        ]
        Tag.objects.bulk_create(tags)
        print('Tags created', datetime.now())

        for i in range(num):
            author_id = i + profiles[0].id
            update_data = profiles_update_data[i]
            Profile.objects.filter(id=author_id).update(
                rating=update_data[0], 
                number_of_moments=update_data[1], 
                number_of_subscribers=update_data[2], 
                number_of_subscriptions=update_data[3]
            )
        print('Finished updating users', datetime.now())
