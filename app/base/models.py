from django.db import models
from django.contrib.auth.models import User
# Create your models here.
"""
Every time we create a model we need to make migrations. to make changes in the database.
to see the table in the admin url we need to add our Room model in our admin.py file
"""

class Topic(models.Model):
    name = models.CharField(max_length=200)
    def __str__(self):
        return self.name


"""
# this will create Room table with the columns: host, topic, name, description, participants, updated, created
# now every time we will create a object, those will be added as the rows.
"""
class Room(models.Model):
    host = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    topic = models.ForeignKey(Topic, on_delete=models.SET_NULL, null=True)
    name = models.CharField(max_length=200)
    description = models.TextField(null = True, blank=True)
    participants = models.ManyToManyField(User, related_name='participants', blank=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-created']
    """
    # this will create a string representation of the object
    """
    def __str__(self):
        return self.name
    
class Message(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    body = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.body