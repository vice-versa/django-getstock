from django.conf.urls.defaults import *
from views import *

urlpatterns = patterns('',
    # Example:
    (r'main/', main, {}, 'main'),
    (r'stockquotes/(?P<code>\w+)/', get_ajax_price, {}, 'stockquotes')

)