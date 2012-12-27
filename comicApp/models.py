from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User
import datetime


class Category(models.Model):
    name = models.CharField(max_length=200, unique=True)
    def __unicode__(self):
        return self.name

class User(models.Model):
    # user = models.OneToOneField(User)
    name = models.CharField(max_length=200, unique=True)
    def __unicode__(self):
        return self.name

class Event(models.Model):
    title = models.CharField(max_length=200)
    date = models.DateField('event date')
    categories = models.ManyToManyField(Category)
    slug = models.SlugField(blank=True)
    def __unicode__(self):
        return self.title
    def save(self, **kwargs):
	super(Event, self).save()
        self.slug = "%i_%i_%i_%i" % (self.date.year, self.date.month, self.date.day, self.id)
        super(Event, self).save()

class Comic(models.Model):
    image = models.ImageField(upload_to="images/comics/", help_text="comic image")
    description = models.TextField(blank=True)
    pub_date = models.DateTimeField(editable=False)
    mod_date = models.DateTimeField(blank=True)
    user = models.ForeignKey('User')
    author = models.CharField(max_length=200, blank=True)
    author_link = models.CharField(max_length=200, blank=True)
    event = models.ForeignKey('Event')
    votes_up = models.IntegerField(default=0, blank=True)
    votes_down = models.IntegerField(default=0, blank=True)
    intervall_start = models.DateField(blank=True, null=True)
    intervall_end = models.DateField(blank=True, null=True)
    def __unicode__(self):
        return self.description
    def save(self, *args, **kwargs):
        if not self.id:
            self.pub_date = datetime.datetime.today()
        self.mod_date = datetime.datetime.today()
        super(Comic, self).save(*args, **kwargs)