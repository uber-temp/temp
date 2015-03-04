from django.conf.urls import patterns, include, url
from django.contrib import admin
from rest_framework import routers
from movies import views
from django.views.decorators.cache import cache_page

router = routers.DefaultRouter()
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'uber.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),
    url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    #api routes
    url(r'^api/v1/movies/$', views.get_movies),
    url(r'^api/v1/movies/(?P<obj_id>[0-9]+)$', views.get_movie),
    url(r'^api/v1/locations/$', views.get_locations),
)
