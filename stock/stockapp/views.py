# Create your views here.

from django.utils import simplejson

from .ystockquote import get_price
from django.http import HttpResponse
from django.template.context import RequestContext
from django.shortcuts import render_to_response


from django.conf import settings
from django.http import HttpResponseRedirect
from django.contrib.auth import login, authenticate, logout

import oauthtwitter 
from oauth import oauth
from django.core.urlresolvers import reverse
from django.views.generic.simple import direct_to_template

def hello(request):
    return direct_to_template(request, 'hello.html')

def main(request):
    
    context = {'user':request.user}                        
                             
    if request.method == 'POST':
        price = get_price('goog')
        context['price'] = price 
    context = RequestContext(request, context)
    
    return render_to_response('main.html', context)

def get_ajax_price(request, code):
    
    result = dict(price=get_price(code))
    return HttpResponse(simplejson.dumps(result))

CONSUMER_KEY = getattr(settings, 'TWITTER_CONSUMER_KEY', 'YOUR_KEY')
CONSUMER_SECRET = getattr(settings, 'TWITTER_CONSUMER_SECRET', 'YOUR_SECRET')

def twitter_signin(request):
    twitter = oauthtwitter.OAuthApi(CONSUMER_KEY, CONSUMER_SECRET)
    request_token = twitter.getRequestToken()
    request.session['request_token'] = request_token.to_string()
    signin_url = twitter.getAuthorizationURL(request_token)
    return HttpResponseRedirect(signin_url)

def twitter_return(request):
    request_token = request.session.get('request_token', None)
    # If there is no request_token for session,
    #    means we didn't redirect user to twitter
    if not request_token:
        # Redirect the user to the login page,
        # So the user can click on the sign-in with twitter button
        return HttpResponse("We didn't redirect you to twitter...")

    token = oauth.OAuthToken.from_string(request_token)

    # If the token from session and token from twitter does not match
    #   means something bad happened to tokens
    if token.key != request.GET.get('oauth_token', 'no-token'):
        del request.session['request_token']
        # Redirect the user to the login page
        return HttpResponse("Something wrong! Tokens do not match...")

    twitter = oauthtwitter.OAuthApi(CONSUMER_KEY, CONSUMER_SECRET, token)
    access_token = twitter.getAccessToken()

    request.session['access_token'] = access_token.to_string()
    auth_user = authenticate(access_token=access_token)

    # if user is authenticated then login user
    if auth_user:
        login(request, auth_user)
    else:
        # We were not able to authenticate user
        # Redirect to login page
        del request.session['access_token']
        del request.session['request_token']
        return HttpResponse("Unable to authenticate you!")

    # authentication was successful, use is now logged in
    return HttpResponseRedirect(reverse('main'))


def twitter_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('main'))