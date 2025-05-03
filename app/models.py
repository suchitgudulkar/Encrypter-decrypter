from django.db import models
from django.contrib.auth.models import User

SOURCE_CHOICES = (
    ('DIMA Employee', 'DIMA Employee'),
    ('Github', 'Github'),
    ('DIMA Partner', 'DIMA Partner'),
    ('News Paper Ad', 'News Paper Ad'),
    ('Social Media', 'Social Media'),
    ('Others', 'Others'),
)

class User_Profile(models.Model):
    username = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    full_name = models.CharField(max_length=100, null=True, blank=True)
    contact = models.CharField(max_length=200, null=True, blank=True)
    email = models.CharField(max_length=200, null=True, blank=True)
    address = models.CharField(max_length=200, null=True, blank=True)
    city = models.CharField(max_length=200, null=True, blank=True)
    state = models.CharField(max_length=200, null=True, blank=True)
    country = models.CharField(max_length=200, null=True, blank=True)
    pincode = models.CharField(max_length=100, null=True, blank=True)
    source_of_known = models.CharField(max_length=100, choices=SOURCE_CHOICES, null=True, blank=True)

    def __str__(self):
        return self.full_name