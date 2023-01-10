from django.db import models
from django_quill.fields import QuillField
from django.contrib.auth.models import User
from django.utils.text import slugify

# Create your models here.

class Tontine(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, null=False, blank=False, related_name='owner')
    name = models.CharField(max_length = 150, blank=False, null=False)
    slug = models.SlugField(max_length = 150, unique=True, blank=False, null=False)
    creation_date = models.DateTimeField(auto_now=True, auto_now_add=False)
    number_of_members = models.PositiveBigIntegerField(blank=False, null=False)
    members = models.ManyToManyField(User, blank=True, related_name='members')
    slogan = QuillField(blank=False, null=False)
    rules = QuillField(blank=False, null=False)
    
    def __str__(self):
        return f'Tontine #{self.id} : {self.name}'
    
    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        super(Tontine, self).save(*args, **kwargs)
    
    # TODO: Implement the different methods of this class which are
    # - Create
    # - Update
    # - Lookup/Search
    # - Delete
    # - List
    