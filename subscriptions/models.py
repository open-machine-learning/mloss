from markdown import markdown
from django.contrib.auth.models import User
from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

class Subscriptions(models.Model):
    """ 
	Email subscriptions on various events
	
	* software authors should be notified when someone posts a comment to their software package
	* people sending comments to a sw should be notified on answers
	* people should be able to subscribe to threads in the forum
	* email reminder to users, once per quarter of the year, that they are subscribed and which
	software packages are new since their last logon
	* people should see a list of subscriptions on their user page (with unsubscribe option)
	"""

    # user, title, url
    user = models.ForeignKey(User, raw_id_admin=True)
    title = models.CharField(max_length=200)
    url = models.URLField(verify_exists=False)
    # if bookmark == true don't send out notifications
    bookmark = models.BooleanField(default=False)

    # software/posting object etc - this is handled via generic content types
    content_type = models.ForeignKey(ContentType)
    object_id = models.PositiveIntegerField()
    content_object = generic.GenericForeignKey()
    last_updated = models.DateTimeField(auto_now_add=True)
    subscribed_date = models.DateTimeField(auto_now_add=True)


    class Admin:
        list_display = ('user', 'title', 'last_updated', 'subscribed_date', 'url',
                'object_id', 'content_type')
        pass
