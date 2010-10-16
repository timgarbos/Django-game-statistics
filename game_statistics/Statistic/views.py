from game_statistics.Statistic.models import *
from django.template import Context, loader
from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import render_to_response, get_object_or_404
from django.core import serializers
import json

def postentry(request, application_id):
    try:
        p = Application.objects.get(pk=application_id)
    except Place.DoesNotExist:
        raise Http404

    if request.method != 'POST':
        raise Http404
    data = request.POST["data"]
    
    #Check if data is correctly signed in data.signature
    
    realdata = json.loads(data);
    u = StatsUser(name="Unknown",type="Unknown")
    u.save()
    s = Statistic.objects.get(name=realdata['name'],application=p)
    entry = StatisticEntry(value=realdata['value'],user=u,statistic = s)
    entry.save()
    response = HttpResponse()
    return response
    
    
    
def test(request,application_id):
    return render_to_response('test.html', {'id':application_id})
