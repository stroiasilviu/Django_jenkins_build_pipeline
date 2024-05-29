from django.contrib import admin

# Register your models here.
from django.contrib.auth.admin import UserAdmin


# Register your models here.
from ssm_app.models import *

admin.site.register(Playlist)
admin.site.register(Album)
admin.site.register(Genre)
admin.site.register(Artist)
admin.site.register(Song)
admin.site.register(SubscriptionPlan)
admin.site.register(Profile)
