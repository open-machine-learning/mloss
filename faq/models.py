from django.db import models

# Create your models here.
class Faq(models.Model):
    question = models.TextField()
    answer = models.TextField()

    class Admin:
        fields = (
            ('None', {'fields': ('question','answer')}),
            )

        def __str__(self):
            return self.question
        
