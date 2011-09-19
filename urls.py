from django.conf.urls.defaults import *
from django.conf import settings
#from views import cm_login, cm_logout
import logging

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    (r'^app/', include('chemmineng.cmplatform.urls')),
    (r'^admin/(.*)', admin.site.root),
	(r'^accounts/', include('chemmineng.accounts.urls')),
    	(r'^myCompounds/', include('chemmineng.myCompounds.urls')),
	(r'^compounds/', include('chemmineng.compounddb.urls')),
	(r'^screens/', include('chemmineng.screendb.urls')),
	(r'^tree/', include('chemmineng.treeviewer.urls')),
	(r'^similarity/', include('chemmineng.similarityworkbench.urls')),
)

if settings.DEBUG:
    logging.basicConfig(level=logging.DEBUG)
    import os
    root = os.path.dirname(__file__)
    urlpatterns += patterns('', 
		(r'^static/(?P<path>.*)$', 'django.views.static.serve',
				{'document_root': root + '/static'}),
    )

urlpatterns += patterns('', 
	(r'', include('cms.urls')),
)
