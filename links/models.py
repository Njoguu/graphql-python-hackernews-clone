from django.db import models
import django.utils.timezone as tz
from django.conf import settings


# Create your models here.
class Link(models.Model):
    url = models.URLField()
    description = models.TextField(blank=True)
    date_posted = models.DateField(default=tz.now())
    posted_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, on_delete=models.CASCADE)

class Vote(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    link = models.ForeignKey('links.Link', related_name='votes', on_delete=models.CASCADE)