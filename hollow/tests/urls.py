from django.conf.urls.defaults import *

from hollow.tests import admin

urlpatterns = patterns('',
    (r'^', include(admin.site.urls)),
)
