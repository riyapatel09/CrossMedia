from django.contrib.auth.models import User
from django.db import models
from django.dispatch import receiver
from django.db.models.signals import post_save
from datetime import datetime



# Create your models here.
from django.db.models import CASCADE


# class FriendList(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     friend_id = models.PositiveIntegerField(null=True,blank=True)
from django.urls import reverse


class FriendList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friend_of')
    friend = models.ForeignKey(User, on_delete=models.CASCADE, related_name='friend_list')

    class Meta:
        unique_together = ('user','friend')


class SiteGroup(models.Model):
    name = models.CharField(max_length=200, help_text='Enter a Group name', null=True)
    description = models.TextField(max_length=1000, help_text='Enter a Group description', null=True)
    total_member = models.PositiveIntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class GroupMember(models.Model):
    group = models.ForeignKey(SiteGroup, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class Event(models.Model):
    name = models.CharField(max_length=200, help_text='Enter a Event name', null=True)
    description = models.TextField(max_length=1000, help_text='Enter a event description', null=True)
    start_date = models.DateField(null=True)
    end_date = models.DateField(null=True)
    start_time = models.DateTimeField(null=True)
    end_time = models.DateTimeField(null=True)


class Profile(models.Model):
    GENDER_CHOICES = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES,null=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField(null=True, blank=True)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics', null=True, blank=True)
    is_parent = models.BooleanField(blank=True,null=True)
    #age = models.PositiveIntegerField(null=True)
    email_confirmed = models.BooleanField(default=False, null=True)
    #parent_email = models.EmailField(null=True)


    # @receiver(post_save, sender=User)
    # def update_user_profile(sender, instance, created, **kwargs):
    #     if created:
    #         Profile.objects.create(user=instance)
    #     instance.profile.save()
    #first_name = models.TextField(max_length=50, help_text='Enter first name', null=True)
    #last_name = models.TextField(max_length=50, help_text='Enter last name', null=True)
    #birthdate = models.DateField(null=True)
    #gender = models.ChoiceField(widget=models.RadioSelect)

    @receiver(post_save, sender=User)
    def create_profile(sender, instance, created, **kwargs):
        if created:
            Profile.objects.create(user=instance)
        instance.profile.save()


    def __str__(self):
        return f'{self.user.username} Profile'

class Post(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, default=1)
    title = models.CharField(max_length=120)
    image = models.ImageField(null=True, blank=True, upload_to='images')
    content = models.TextField()
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return self.title

    def __unicode__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("crossmedia:detail", kwargs={"id": self.id})

    def number_of_like(self):
        total_like = self.likepost_set.all().count()
        return total_like

class LikePost(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)

class FriendRequestList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sending_request')
    requested_user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='receving_request')

    class Meta:
        unique_together = ('user','requested_user')

class ParentChild(models.Model):
    parent = models.ForeignKey(User, on_delete=models.CASCADE, related_name='parent')
    child = models.ForeignKey(User, on_delete=models.CASCADE, related_name='child')

    class Meta:
        unique_together = ('parent','child')

