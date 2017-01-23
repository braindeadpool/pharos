from __future__ import unicode_literals

import hashlib
import os.path
import urllib

from django.conf import settings
from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.utils.encoding import python_2_unicode_compatible

from bootcamp.activities.models import Notification


@python_2_unicode_compatible
class Profile(models.Model):
    user = models.OneToOneField(User)
    identification = models.CharField(max_length=50)
    role = models.CharField(max_length=50, null=True, blank=True)
    web_page = models.CharField(max_length=50, null=True, blank=True)
    role = models.CharField(max_length=50, null=True, blank=True)
    job_title = models.CharField(max_length=50, null=True, blank=True)
    city = models.CharField(max_length=50, null=True, blank=True)
    state = models.CharField(max_length=50, null=True, blank=True)
    country = models.CharField(max_length=50, null=True, blank=True)
    institution = models.CharField(max_length=50, null=True, blank=True)
    bio = models.CharField(max_length=200, null=True, blank=True)
    isLinkedinPresent = models.NullBooleanField(blank=True)
    linkedin_url = models.URLField(max_length=2000, null=True, blank=True)

    class Meta:
        db_table = 'auth_profile'

    def __str__(self):
        return self.user.username
    
    def get_bio(self):
        return self.bio
    
    def get_linkedIn_profile(self):
        if self.linkedin_url is None:
            return "#"
        return self.linkedin_url    
            
    
    def create_linkedin(self, linkedin_id):
        LinkedInProfile.objects.get_or_create(identifier=linkedin_id,
                                                       user=self)
    def get_url(self):
        web_page = self.web_page
        if "http://" not in self.web_page and "https://" not in self.web_page and len(self.web_page) > 0:  # noqa: E501
            web_page = "http://" + str(self.web_page)

        return web_page

    def get_picture(self):
        no_picture = 'http://trybootcamp.vitorfs.com/static/img/user.png'
        try:
            filename = settings.MEDIA_ROOT + '/profile_pictures/' +\
                self.user.username + '.jpg'
            picture_url = settings.MEDIA_URL + 'profile_pictures/' +\
                self.user.username + '.jpg'
            if os.path.isfile(filename):
                return picture_url
            else:
                gravatar_url = 'http://www.gravatar.com/avatar/{0}?{1}'.format(
                    hashlib.md5(self.user.email.lower()).hexdigest(),
                    urllib.urlencode({'d': no_picture, 's': '256'})
                    )
                return gravatar_url

        except Exception:
            return no_picture

    def get_screen_name(self):
        try:
            if self.user.get_full_name():
                return self.user.get_full_name()
            else:
                return self.user.username
        except:
            return self.user.username

    def notify_liked(self, feed):
        if self.user != feed.user:
            Notification(notification_type=Notification.LIKED,
                         from_user=self.user, to_user=feed.user,
                         feed=feed).save()

    def unotify_liked(self, feed):
        if self.user != feed.user:
            Notification.objects.filter(notification_type=Notification.LIKED,
                                        from_user=self.user, to_user=feed.user,
                                        feed=feed).delete()

    def notify_commented(self, feed):
        if self.user != feed.user:
            Notification(notification_type=Notification.COMMENTED,
                         from_user=self.user, to_user=feed.user,
                         feed=feed).save()

    def notify_also_commented(self, feed):
        comments = feed.get_comments()
        users = []
        for comment in comments:
            if comment.user != self.user and comment.user != feed.user:
                users.append(comment.user.pk)

        users = list(set(users))
        for user in users:
            Notification(notification_type=Notification.ALSO_COMMENTED,
                         from_user=self.user,
                         to_user=User(id=user), feed=feed).save()

    def notify_favorited(self, question):
        if self.user != question.user:
            Notification(notification_type=Notification.FAVORITED,
                         from_user=self.user, to_user=question.user,
                         question=question).save()

    def unotify_favorited(self, question):
        if self.user != question.user:
            Notification.objects.filter(
                notification_type=Notification.FAVORITED,
                from_user=self.user,
                to_user=question.user,
                question=question).delete()

    def notify_answered(self, question):
        if self.user != question.user:
            Notification(notification_type=Notification.ANSWERED,
                         from_user=self.user,
                         to_user=question.user,
                         question=question).save()

    def notify_accepted(self, answer):
        if self.user != answer.user:
            Notification(notification_type=Notification.ACCEPTED_ANSWER,
                         from_user=self.user,
                         to_user=answer.user,
                         answer=answer).save()

    def unotify_accepted(self, answer):
        if self.user != answer.user:
            Notification.objects.filter(
                notification_type=Notification.ACCEPTED_ANSWER,
                from_user=self.user,
                to_user=answer.user,
                answer=answer).delete()


def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)


def save_user_profile(sender, instance, **kwargs):
    instance.profile.save()


class LinkedInProfile(models.Model):
    user = models.ForeignKey(User)
    date = models.DateTimeField(auto_now_add=True)
    identifier = models.CharField(max_length=200, null=True, blank=True)
    
    def __str__(self):
        return self.user.username

# class Lab(models.Model):
#     manager = models.ForeignKey(User)
#     date = models.DateTimeField(auto_now_add=True)
#     name = models.CharField(max_length=200, null=True, blank=True)
#     institution = models.CharField(max_length=200, null=True, blank=True) 
#     building = models.CharField(max_length=200, null=True, blank=True) 
#     city = models.CharField(max_length=50, null=True, blank=True)
#     state = models.CharField(max_length=50, null=True, blank=True)
#     country = models.CharField(max_length=50, null=True, blank=True)
#     
#     def __str__(self):
#         return self.name
#     
# class Device(models.Model):
#     #Lab Manager ID
#     manager = models.ForeignKey(User)
#     date = models.DateTimeField(auto_now_add=True)
#     #Device Name
#     name = models.CharField(max_length=200, null=True, blank=True)
#     lab = models.ForeignKey(Lab)
#     desciption = models.CharField(max_length=1000, null=True, blank=True) 
#     requestor = models.CharField(max_length=200, null=True, blank=True)
#     
#     def __str__(self):
#         return self.name + "  " + self.lab.name
    

post_save.connect(create_user_profile, sender=User)
post_save.connect(save_user_profile, sender=User)
