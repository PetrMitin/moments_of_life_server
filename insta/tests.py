from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework.test import APIClient
from insta.models import *
from insta.serializers import ProfileSerializer
import io
import json
from PIL import Image

# Create your tests here.
class MomentsTests(APITestCase):
    def setUp(self):
        self.user = User(username='test', email='test@test')
        self.user.set_password(raw_password='test')
        self.user.save()
        self.profile = Profile.objects.create(user=self.user)
        self.profile_data = {
            'id': self.profile.id
        }
        self.moment = Moment.objects.create_moment('Test title #test', 'Test', self.profile_data, None)
        Tag.objects.create(moment=self.moment, tag='#test')
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)
        self.image = self.generate_photo_file()
    
    def generate_photo_file(self):
        file = io.BytesIO()
        image = Image.new('RGBA', size=(100, 100), color=(155, 0, 0))
        image.save(file, 'png')
        file.name = 'test.png'
        file.seek(0)
        return file
    
    def test_create_moment(self):
        """test moment creation process"""
        url = reverse('create_moment')
        profile_data = ProfileSerializer(self.profile).data
        bad_res = self.client.post(url)
        self.assertEqual(bad_res.status_code, 400)
        
        response = self.client.post(url, {
            'title': 'Test title', 
            'content': 'Test content #test',
            'image': self.image,
            'author': json.dumps(profile_data)}, format='multipart')
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Moment.objects.last().title, 'Test title')
        self.assertEqual(Profile.objects.first().number_of_moments, 2)
        os.remove(Moment.objects.last().image.path)
    
    def test_get_moments_of_profile(self):
        """test functionality of getting moments of authenticated user profile"""
        url = reverse('moments_by_profile', args=[self.profile.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        
        bad_url = reverse('moments_by_profile', args=[123112])
        bad_res = self.client.get(bad_url)
        self.assertEqual(bad_res.status_code, 400)
        
        
    def test_get_moments_by_tag(self):
        """user should be able to search for moments that have specific tags"""
        url = reverse('moments_by_tag') + f'?query=#test'
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        
        bad_url = reverse('moments_by_tag') + f'?query=#test123'
        bad_res = self.client.get(bad_url)
        self.assertEqual(len(bad_res.json()), 0)
        
    def test_create_comment(self):
        """test comment creation process"""
        url = reverse('create_comment')
        bad_res = self.client.post(url)
        self.assertEqual(bad_res.status_code, 400)
        
        response = self.client.post(url, {
            'content': 'test comment',
            'author': self.profile_data,
            'moment_id': self.moment.id
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(Comment.objects.filter(moment=self.moment)), 1)
        

class ProfileTests(APITestCase):
    def setUp(self):
        self.user = User(username='test', email='test@test')
        self.user.set_password(raw_password='test')
        self.user.save()
        self.profile = Profile.objects.create(user=self.user)
    
    def test_registration(self):
        """test registration process"""
        moments_url = reverse('moments_by_profile', args=[self.profile.id])
        bad_moments_response = self.client.get(moments_url)
        self.assertEqual(bad_moments_response.status_code, 403)

        url = reverse('registration')
        response = self.client.post(url, {
            'email': 'test1@test1',
            'password': 'test1',
            'username': 'test1',
            'avatar': ''
        })
        self.assertEqual(response.status_code, 200)
        cookies = dict(response.client.cookies.items())
        user = User.objects.filter(email='test1@test1').first()
        self.assertTrue(user)
        self.assertTrue(cookies['sessionid'])
        self.assertTrue(cookies['csrftoken'])
        self.client.credentials(sessionid=cookies['sessionid'], csrftoken=cookies['csrftoken'])
        
        moments_url = reverse('moments_by_profile', args=[self.profile.id])
        good_moments_response = self.client.get(moments_url)
        self.assertEqual(good_moments_response.status_code, 200)
        
    def test_login(self):
        """test login functionality"""
        moments_url = reverse('moments_by_profile', args=[self.profile.id])
        bad_response = self.client.get(moments_url)
        self.assertEqual(bad_response.status_code, 403)
        
        url = reverse('login')
        response = self.client.post(url, {
            'email': 'test@test',
            'password': 'test'
        })
        self.assertEqual(response.status_code, 200)
        cookies = dict(response.client.cookies.items())
        self.assertTrue(cookies['sessionid'])
        self.assertTrue(cookies['csrftoken'])
        self.client.credentials(sessionid=cookies['sessionid'], csrftoken=cookies['csrftoken'])
        
        moments_url = reverse('moments_by_profile', args=[self.profile.id])
        good_response = self.client.get(moments_url)
        self.assertEqual(good_response.status_code, 200)
        
    def test_logout(self):
        """test logout functionality"""
        url = reverse('logout')
        response = self.client.post(url)
        self.assertEqual(response.status_code, 403)
        
        self.client.force_authenticate(user=self.user)
        response = self.client.post(url)
        self.assertEqual(response.status_code, 200)
    
    def test_profile_update(self):
        """test profile update functionality"""
        url = reverse('update_profile', args=[self.profile.id])
        self.client.force_authenticate(user=self.user)
        response = self.client.put(url, {
            'username': 'test14'
        })
        self.assertEqual(response.status_code, 200)
        user = User.objects.filter(username='test14').first()
        self.assertTrue(user)
    
    def test_search_profiles_by_username(self):
        """test search functionality"""
        url = reverse('profiles_by_username') + '?query=test'
        self.client.force_authenticate(user=self.user)
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)

class EventsTests(APITestCase):
    def setUp(self):
        self.user1 = User(username='test1', email='test1@test1')
        self.user1.set_password(raw_password='test1')
        self.user1.save()
        self.profile1 = Profile.objects.create(user=self.user1)
        self.user2 = User(username='test2', email='test2@test2')
        self.user2.set_password(raw_password='test2')
        self.user2.save()
        self.profile2 = Profile.objects.create(user=self.user2)
        self.profile1_data = {
            'id': self.profile1.id
        }
        self.profile2_data = {
            'id': self.profile2.id
        }
        self.moment = Moment.objects.create_moment('Moment', 'Moment', self.profile1_data, None)
        self.comment = Comment.objects.create(content='Comment', author=self.profile1, moment=self.moment)
        self.client = APIClient()
        self.client.force_authenticate(user=self.user1)
    
    def test_get_user_events(self):
        """get users moment likes, comment likes and subscriptions"""
        MomentLike.objects.create(author=self.profile1, moment=self.moment)
        CommentLike.objects.create(author=self.profile2, comment=self.comment)
        Subscription.objects.create(author=self.profile1, subscriber=self.profile2)
        url = reverse('events_by_profile')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        json_res = response.json()
        self.assertEqual(len(json_res.get('moment_like_events')), 1)
        self.assertEqual(len(json_res.get('comment_like_events')), 1)
        self.assertEqual(len(json_res.get('subscription_events')), 1)
    
    def test_create_moment_like(self):
        """like user moment"""
        url = reverse('like_moment')
        response = self.client.post(url, {
            'moment_id': self.moment.id,
            'author_id': self.profile2.id
        })
        self.assertEqual(response.status_code, 200)
        profile1_updated = Profile.objects.get(id=self.profile1.id)
        self.assertEqual(profile1_updated.rating, 1)

    def test_delete_moment_like(self):
        """unlike user moment"""
        MomentLike.objects.create(author=self.profile2, moment=self.moment)
        url = reverse('unlike_moment')
        response = self.client.delete(url, {
            'moment_id': self.moment.id,
            'author_id': self.profile2.id
        })
        self.assertEqual(response.status_code, 200)
        profile1_updated = Profile.objects.get(id=self.profile1.id)
        self.assertEqual(profile1_updated.rating, 0)
    
    def test_create_comment_like(self):
        """like user comment"""
        url = reverse('like_comment')
        response = self.client.post(url, {
            'comment_id': self.comment.id,
            'author_id': self.profile2.id
        })
        self.assertEqual(response.status_code, 200)
        profile1_updated = Profile.objects.get(id=self.profile1.id)
        self.assertEqual(profile1_updated.rating, 1)
    
    def test_delete_comment_like(self):
        """unlike user comment"""
        CommentLike.objects.create(author=self.profile2, comment=self.comment)
        url = reverse('unlike_comment')
        response = self.client.delete(url, {
            'comment_id': self.comment.id,
            'author_id': self.profile2.id
        })
        self.assertEqual(response.status_code, 200)
        profile1_updated = Profile.objects.get(id=self.profile1.id)
        self.assertEqual(profile1_updated.rating, 0)
    
    def test_subscribe(self):
        """subscribe to user"""
        url = reverse('subscribe')
        response = self.client.post(url, {
            'subscriber_id': self.profile2.id,
            'author_id': self.profile1.id
        })
        self.assertEqual(response.status_code, 200)
        profile1_updated = Profile.objects.get(id=self.profile1.id)
        self.assertEqual(profile1_updated.number_of_subscribers, 1)
        profile2_updated = Profile.objects.get(id=self.profile2.id)
        self.assertEqual(profile2_updated.number_of_subscriptions, 1)
    
    def test_unsubscribe(self):
        """unsubscribe to user"""
        Subscription.objects.create(author=self.profile1, subscriber=self.profile2)
        url = reverse('unsubscribe')
        response = self.client.delete(url, {
            'subscriber_id': self.profile2.id,
            'author_id': self.profile1.id
        })
        self.assertEqual(response.status_code, 200)
        profile1_updated = Profile.objects.get(id=self.profile1.id)
        self.assertEqual(profile1_updated.number_of_subscribers, 0)
        profile2_updated = Profile.objects.get(id=self.profile2.id)
        self.assertEqual(profile2_updated.number_of_subscriptions, 0)
    
    def test_get_moments_of_user_subs(self):
        """tests functionality of getting moments of users 
        to which authenticated user is subscribed"""
        Subscription.objects.create(author=self.profile2, subscriber=self.profile1)
        Moment.objects.create_moment('Moment', 'Moment', self.profile2_data, None)
        url = reverse('moments_by_subscriptions')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.json()), 1)
        