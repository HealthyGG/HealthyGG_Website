from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from taggit.managers import TaggableManager

# Create your models here.
class Subject(models.Model):
    title = models.CharField(max_length=100)
    slug = models.SlugField(max_length=200, unique=True)

    class Meta:
        ordering = ('title',)

    def __str__(self):
        return self.title

class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    subject = models.ForeignKey(Subject, related_name='posts', on_delete=models.PROTECT, null=True)
    title = models.CharField(max_length=250)
    image = models.ImageField(default = 'default.jpg', upload_to='images') 
    slug = models.SlugField(max_length=250, unique_for_date='publish')
    author = models.ManyToManyField(User, blank=False, related_name='blog_posts')
    content = models.TextField(blank=False, null=False)
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    tags = TaggableManager()

    class Meta:
        ordering = ('-publish',)

    def __str__(self):
        return self.title

class Video(models.Model):
    embed_url = models.CharField(max_length=128)