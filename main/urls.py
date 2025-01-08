from django.urls import path, re_path
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.views.static import serve
from . import views

app_name = 'main'


urlpatterns = [
    #re_path(r'^$', views.home, name='home'),
    re_path(r'^$', views.linking, name='home'),
    path('login/', views.login, name='login'),
    path('linking/', views.linking, name='linking'),
    path('settings/', views.settings, name='settings'),
    path('currentLink/', views.currentLink, name='currentLink'),
    path('getMetadata/', views.getMetadata, name='getMetadata'),
    path('logout/', views.logout_view, name='logout_view'),
    path('saveElementsAndLinks/', views.saveElementsAndLinks, name='saveElementsAndLinks'),
    path('saveSettings/', views.saveSettings, name='saveSettings'),
    path('removeSettings/', views.removeSettings, name='removeSettings'),
    path('removeLinks/', views.removeLinks, name='removeLinks'),
    path('populateTable/', views.populateTable, name='populateTable'),
    re_path(r'^static/(?P<path>.*)$', serve,{'document_root': settings.STATIC_ROOT})
    ] + staticfiles_urlpatterns()
