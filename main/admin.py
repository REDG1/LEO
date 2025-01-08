from django.contrib import admin

# Register your models here.
from django.contrib.sessions.models import Session
from main.models import *

admin.site.register(Session)
admin.site.register(DataProvider)
admin.site.register(Element)
admin.site.register(Link)
admin.site.register(ProviderUserSetting)


