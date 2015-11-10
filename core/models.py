from django.db import models
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

# Create your models here.
class Stock(models.Model):
    symbol = models.CharField(max_length=300)
    company = models.CharField(max_length=300)
    description = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User)

    def __unicode__(self):
        return self.company

    def get_absolute_url(self):
        return reverse("stock_detail", args=[self.id])

class Review(models.Model):
    stock = models.ForeignKey(Stock)
    user = models.ForeignKey(User)
    created_at = models.DateTimeField(auto_now_add=True)
    text = models.TextField()

    def __unicode__(self):
        return self.text

class Vote(models.Model):
    user = models.ForeignKey(User)
    stock = models.ForeignKey(Stock, blank=True, null=True)
    review = models.ForeignKey(Review, blank=True, null=True)

    def __unicode__(self):
        return "%s upvoted" % (self.user.username)