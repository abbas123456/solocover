from django.db import models

class Vote(models.Model):
    score = models.IntegerField()
    comment = models.CharField(max_length=64)
    created_date = models.DateTimeField()
    
    def __unicode__(self):
        return self.comment