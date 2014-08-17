from django.conf.urls import patterns, include, url
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns(
    '',
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'cards.views.index', name='index'),
    url(r'^login', 'cards.views.user_login'),
    url(r'^logout', 'cards.views.user_logout'),
    )

urlpatterns += staticfiles_urlpatterns()
