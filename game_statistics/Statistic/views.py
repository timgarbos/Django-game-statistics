from game_statistics.Statistic.models import *
from django.template import Context, loader
from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt

from django.views.generic.simple import direct_to_template
import facebook.djangofb as facebook
try:
    import json
except ImportError:
    import simplejson as json 

@csrf_exempt
def postentry(request):


    if request.method != 'POST':
        raise Http404
    data = request.POST["data"]
    
    #Check if data is correctly signed in data.signature
    
    realdata = json.loads(data);

    try:
        p = Application.objects.get(pk=realdata['appid'])
    except Place.DoesNotExist:
        raise Http404
    
    u = StatsUser(name='unknown',type='facebook',uid=realdata['uid'])
    u.save()
    s = Statistic.objects.get(name=realdata['name'],application=p)
    entry = StatisticEntry(value=realdata['value'],user=u,statistic = s)
    entry.save()
    response = HttpResponse()
    return response
    
    
    
def test(request):
    return render_to_response('test.html', {})


def fb_highscore(request,statistic_id):
    return render_to_response('test.html', {})

@facebook.require_login()
def fb_canvas(request,app_id,stat_name):

    try:
        p = Application.objects.get(pk=app_id)
    except Place.DoesNotExist:
        raise Http404
    try:
        s = Statistic.objects.get(name=stat_name,application=p)
    except Place.DoesNotExist:
        raise Http404
    
    
    #Lets get friends who has added the app
    friends = request.facebook.fql.query("SELECT uid FROM user WHERE has_added_app=1 and uid IN (SELECT uid2 FROM friend WHERE uid1 = "+request.facebook.uid+")")
    friends.append({u'uid':request.facebook.uid})
    highscore = StatisticEntry.objects.filter(statistic=s).filter(user__uid__in=friends.values)
    return direct_to_template(request, 'canvas.html', extra_context={'uid': request.facebook.uid,'highscore':highscore})
