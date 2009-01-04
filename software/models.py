import datetime
from django.utils.html import strip_tags
from django.contrib.contenttypes.models import ContentType
from django.contrib.comments.models import Comment
from django.contrib.auth.models import User
from django.contrib.sites.models import Site
from django.core.exceptions import ObjectDoesNotExist
from django.db import models
from django.shortcuts import get_object_or_404
from django.contrib.comments.signals import comment_was_posted

from markdown import markdown
from utils import send_mails
from subscriptions.models import Subscriptions

# Create your models here.
class Software(models.Model):
    """
    A description of some machine learning open source
    software project.
    """
    user = models.ForeignKey(User)
    title = models.CharField(max_length=80)

    average_rating = models.FloatField(editable=False, default=-1)
    average_features_rating = models.FloatField(editable=False, default=-1)
    average_usability_rating = models.FloatField(editable=False, default=-1)
    average_documentation_rating = models.FloatField(editable=False, default=-1)
    total_number_of_votes = models.IntegerField(editable=False, default=0)

    total_number_of_views = models.IntegerField(editable=True, default=0)
    total_number_of_downloads = models.IntegerField(editable=True, default=0)

    def save(self, **kwargs):
        new_software = not self.id
        silent_update =  kwargs.has_key('silent_update')
        if silent_update:
            kwargs.pop('silent_update')
        if not self.total_number_of_downloads:
            self.total_number_of_downloads=0
        if not self.total_number_of_views:
            self.total_number_of_views=0

        # Use safe_mode in Markdown to prevent arbitrary input
        # and strip all html tags from CharFields
        self.title = strip_tags(self.title)
        super(Software, self).save(kwargs)

        if new_software and not silent_update:
            self.subscribe(self.user, bookmark=False)

    def subscribe(self, user, bookmark):
        ctype = ContentType.objects.get_for_model(self)
        Subscriptions.objects.get_or_create(title="Software " + self.title,
                content_type=ctype, object_id=self.id, user=user,
                url=self.get_absolute_url(), bookmark=bookmark)

    def unsubscribe(self, user, bookmark):
        ctype = ContentType.objects.get_for_model(self)
        object=get_object_or_404(Subscriptions, content_type=ctype, object_id=self.id,
                user=user, bookmark=bookmark)
        object.delete()

    def get_subscription_count(self):
        ctype = ContentType.objects.get_for_model(self)
        return Subscriptions.objects.filter(content_type=ctype, object_id=self.id).count()

    def notify_update(self):
        ctype = ContentType.objects.get_for_model(self)
        subscribers=Subscriptions.objects.filter(content_type=ctype, object_id=self.id)

        subject='Updates on mloss.org software project ' + self.title
        message='''Dear mloss.org user,

you are receiving this email as you have subscribed to the "'''

        message+=self.title
        message+='''" software project,
which has just been updated.

Feel free to visit mloss.org to see what has changed.

        '''
        message+='http://%s%s' % (Site.objects.get_current().domain, self.get_absolute_url())
        message+='''

Friendly,
   your mloss.org team.
        '''

        send_mails(subscribers, subject, message)

    def get_num_comments(self):
        ctype = ContentType.objects.get_for_model(self)
        return Comment.objects.filter(content_type=ctype, object_pk=self.pk).count()
    def get_last_comments_url(self):
        ctype = ContentType.objects.get_for_model(self)
        u=Comment.objects.filter(content_type=ctype, object_pk=self.pk).order_by('-submit_date')
        if u.count():
            return u[0].get_absolute_url()
        else:
            return self.get_absolute_url()

    def get_description_page(self):
        s="<html>" + self.description_html + "</html>"
        return s.encode('utf-8')

    def __unicode__(self):
        return unicode(self.title)

    def get_absolute_url(self):
        return ('software.views.entry.software_detail', (), { 'software_id': str(self.id) })

    get_absolute_url = models.permalink(get_absolute_url)

    def get_stats_for_today(self):
        t = datetime.date.today().strftime("%Y-%m-%d")
        stats, flag = SoftwareStatistics.objects.get_or_create(software=self, date=t)
        return stats

    def update_views(self):
        if self.total_number_of_views:
            self.total_number_of_views += 1
        else:
            self.total_number_of_views = 1

        self.save()
        e=self.get_stats_for_today()
        e.update_views()
        return e

    def update_downloads(self):
        if self.total_number_of_downloads:
            self.total_number_of_downloads += 1
        else:
            self.total_number_of_downloads = 1

        self.save()
        e=self.get_stats_for_today()
        e.update_downloads()

    def get_latest_revision(self):
        from revision.models import Revision
        return get_object_or_404(Revision, software=self, revision=0)

    def increment_revisions(self):
        from revision.models import Revision
        allsoft = Revision.objects.filter(software=self)
        for s in allsoft:
            s.revision+=1
            s.save(silent_update=True)

class SoftwareRating(models.Model):
    """Rating for a software

    Each user can rate a software only once (but she might change
    her rating?)"""
    user = models.ForeignKey(User)
    software = models.ForeignKey(Software)
    features = models.IntegerField(default=0)
    usability = models.IntegerField(default=0)
    documentation = models.IntegerField(default=0)

    def update_software_ratings(self):
        s=self.software
        ratings = SoftwareRating.objects.filter(software=s)

        l = float(len(ratings))
        f=u=d=0
        for r in ratings:
            f+= r.features
            u+= r.usability
            d+= r.documentation

        s.average_rating = (f+u+d)/(3.0*l)
        s.average_features_rating = float(f)/l
        s.average_usability_rating = float(u)/l
        s.average_documentation_rating = float(d)/l
        s.total_number_of_votes = l
        s.save()

    def update_rating(self, f, u, d):

        self.features = f
        self.usability = u
        self.documentation = d
        self.save()
        self.update_software_ratings()

class SoftwareStatistics(models.Model):
    """
    Statistics about a software project
    """
    software = models.ForeignKey(Software)
    date = models.DateField()
    number_of_views = models.IntegerField(default=0)
    number_of_downloads = models.IntegerField(default=0)

    def update_views(self):
        self.number_of_views += 1
        self.save()

    def update_downloads(self):
        self.number_of_downloads += 1
        self.save()

def comment_notification(**kwargs):
    """
         instance is the comment object
    """

    sender=kwargs['sender']
    comment=kwargs['comment']

    try:
        sw=comment.content_object
        ctype = ContentType.objects.get_for_model(sw)
        subscribers=Subscriptions.objects.filter(content_type=ctype, object_id=sw.id)

        if ctype.name and ctype.name == u'software':
            subject='New comment on mloss.org software project ' + sw.title
            message='''Dear mloss.org user,

you are receiving this email as you have subscribed to the "'''

            message+=sw.title
            message+='''" software project,
for which a new comment has just been posted.

Feel free to visit mloss.org to see what has changed.

    '''
        else:
            return # no comment notification for objects other than software yet

        message+='http://%s%s' % (Site.objects.get_current().domain, comment.get_absolute_url())
        message+='''

Friendly,
   your mloss.org team.
        '''

        send_mails(subscribers, subject, message)
    except ObjectDoesNotExist:
        pass

comment_was_posted.connect(comment_notification)
