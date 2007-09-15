"""
Custom managers for most of the models; these add useful logic for
various custom filters and queries.

"""

from django.db import models


class SoftwareManager(models.Manager):
    """
    Custom manager for the Software model.
    
    Adds shortcuts for common filtering operations, and for retrieving
    popular related objects.
    
    """
    def get_by_author(self, username):
        """
        Returns a QuerySet of Snippets submitted by a particular User.
        
        """
        return self.filter(author__username__exact=username)
    
