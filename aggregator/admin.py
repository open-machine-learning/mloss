from django.contrib import admin
from aggregator.models import Feed

class FeedAdmin(admin.ModelAdmin):
	pass

admin.site.register(Feed, FeedAdmin)
