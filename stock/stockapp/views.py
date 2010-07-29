# Create your views here.

from django.http import HttpResponse
from django.views.generic.simple import direct_to_template
from django.utils import simplejson

from .ystockquote import get_price


def main(request):
    
    extra_context = dict(csrf=request)
    if request.method == 'POST':
        price = get_price('goog')
        extra_context['price'] = price 
    return direct_to_template(request, 'main.html', extra_context)

def get_ajax_price(request, code):
    
    result = dict(price=get_price(code))
    return HttpResponse(simplejson.dumps(result))