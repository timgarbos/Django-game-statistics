from game_statistics.Statistic.models import *
from django.template import Context, loader
from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
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

    u = StatsUser(name="Unknown",type="Unknown")
    u.save()
    s = Statistic.objects.get(name=realdata['name'],application=p)
    entry = StatisticEntry(value=realdata['value'],user=u,statistic = s)
    entry.save()
    response = HttpResponse()
    return response
    
    
    
def test(request):
    return render_to_response('test.html', {})
