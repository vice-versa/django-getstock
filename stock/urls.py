from django.conf.urls.defaults import *
from django.conf import settings

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
from stock.stockapp.views import twitter_signin, twitter_return, twitter_logout, hello

admin.autodiscover()


urlpatterns = patterns('',
    # Example:
    (r'^stock/', include('stock.stockapp.urls')),
    url('^login/$', twitter_signin, name='login'),
    url('^return/$', twitter_return, name='return'),
    url('^logout/$', twitter_logout, name='logout'),
    url('^hello/$', hello, name='hello'),
    
    (r'^admin/', include(admin.site.urls)),
    
    (r'^assets/(?P<path>.*)$', 'django.views.static.serve',
        {'document_root': settings.MEDIA_ROOT}),

)
