from django.contrib import admin
from crossmedia.models import FriendList, SiteGroup, GroupMember, Event, Profile, Post, FriendRequestList, ParentChild

# Register your models here.

admin.site.register(FriendList)
admin.site.register(SiteGroup)
admin.site.register(GroupMember)
admin.site.register(Event)
admin.site.register(Profile)
admin.site.register(Post)
admin.site.register(FriendRequestList)
admin.site.register(ParentChild)

