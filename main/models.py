from django.db import models
from django.contrib.auth.models import User
from django.conf import settings





class DataProvider(models.Model):
    name = models.CharField(max_length=255, null=True, unique=True)

    def __str__(self):
        return f'Name:{self.name}'

class ProviderUserSetting(models.Model):
    host = models.CharField(max_length=255, null=True)
    API_key = models.CharField(max_length=255, null=True, blank=True)
    provider = models.ForeignKey("DataProvider", null=True, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

    class Meta:
        unique_together = ('host', 'provider','user')

    def __str__(self):
        return f'Provider:{self.provider} - User:{self.user}'


class Element(models.Model):

    name = models.CharField(max_length=255, null=True)
    provider = models.ForeignKey("ProviderUserSetting", on_delete=models.CASCADE)
    type = models.CharField(max_length=255, null=True)
    parent = models.ForeignKey("self", null=True, on_delete=models.CASCADE)
    id_inside_Data_Provider = models.IntegerField()

    def __str__(self):
        return f'Name:{self.name} - Type:{self.type} - Provider:{self.provider}'


class Link(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    Element2link = models.ManyToManyField("Element")

    def __str__(self):
        return f'ID:{self.id} - User:{self.user}'
