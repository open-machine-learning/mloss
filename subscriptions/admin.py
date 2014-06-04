from django.contrib import admin
from subscriptions.models import Subscriptions

class SubscriptionsAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'last_updated', 'subscribed_date', 'url',
            'object_id', 'content_type', 'bookmark')

admin.site.register(Subscriptions, SubscriptionsAdmin)

