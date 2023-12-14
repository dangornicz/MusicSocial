from django.contrib import admin

from social.models import SavedEvent, Comment, Followers, Bio

admin.site.register(SavedEvent)
admin.site.register(Comment)
admin.site.register(Followers)
admin.site.register(Bio)
