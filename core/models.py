from django.db import models
from django_quill.fields import QuillField

# Create your models here.

class Tontine(models.Model):
    
    name = models.CharField(max_length = 150, blank=False, null=False)
    creation_date = models.DateTimeField(auto_now=True, auto_now_add=False)
    number_of_members = models.PositiveBigIntegerField(blank=False, null=False)
    slogan = QuillField(blank=False, null=False)
    rules = QuillField(blank=False, null=False)
    
    def __str__(self):
        return f'Tontine #{self.id} : {self.name}'
    
    # TODO: Implement the different methods of this class which are
    # - Create
    # - Update
    # - Lookup/Search
    # - Delete
    # - List
    