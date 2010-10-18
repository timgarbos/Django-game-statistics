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
    
    
    
    realdata = json.loads(data)
    #Check if data is correctly signed in data.signature

    try:
        p = Application.objects.get(pk=realdata['appid'])
    except Application.DoesNotExist:
        raise Http404
    
    u, created = StatsUser.objects.get_or_create(type='facebook',uid=realdata['uid'], defaults={'name': 'fb user'})
    if created:
        u.save()
    s = Statistic.objects.get(name=realdata['name'],application=p)
    entry = StatisticEntry(value=realdata['value'],user=u,statistic = s)
    entry.save()
    response = HttpResponse()
    return response
    
    
    
def getHighscores(request,leaderboard_id):
    
    #Let's find the statistics id
    board = LeaderBoard.objects.get(pk=leaderboard_id)
    #Lets get friends who has added the app
    friends = request.facebook.fql.query("SELECT uid FROM user WHERE has_added_app=1 and uid IN (SELECT uid2 FROM friend WHERE uid1 = "+str(request.facebook.uid)+")")
    friends.append({u'uid':request.facebook.uid})
    highscore = []
    for f in friends:
        scores = StatisticEntry.objects.filter(statistic__id=board.statistic.id).filter(user__uid=f.get('uid')).order_by('-value')
        if scores.count() > 0:
            highscore.append(scores[0])
    highscore.sort(key=lambda x: x.value, reverse=True)
    return highscore
    
def test(request):
    return render_to_response('test.html', {})

@facebook.require_login()
def fb_highscore(request,leaderboard_id):
    
    highscore = getHighscores(request,leaderboard_id)
    return render_to_response('fbhighscore.html', {'highscore':highscore})

@csrf_exempt
@facebook.require_login()
def fb_canvas(request,app_id,leaderboard_id):

   
    
    
    highscore = getHighscores(request,leaderboard_id)
    return direct_to_template(request, 'canvas.html', extra_context={'uid': request.facebook.uid,'highscore':highscore,'statistics_id':s.id})
    
@facebook.require_login()
def invite_friends(request):
    #HTML escape function for invitation content.
    from cgi import escape

    facebook_uid = request.facebook.uid
    # Convert the array of friends into a comma-delimeted string.  
    exclude_ids = ",".join([str(a) for a in request.facebook.friends.getAppUsers()])

    # Prepare the invitation text that all invited users will receive.  
    content = """Show <fb:name uid="%s" firstnameonly="true" shownetwork="false"/> that your friendship means something to you by crashing robots into eachother.
        
             <fb:req-choice url="%s"
     label="Accept and play!"/>
     """ % (facebook_uid, request.facebook.get_add_url())

    invitation_content = escape(content, True)

    return render_to_response('invite.html',
                               {'content': invitation_content, 'exclude_ids': exclude_ids })


def achievements(request,app_id, user_id):
    achieved = UserAchievement.objects.filter(user__id=user_id,achievement__application__id=app_id)
    noImageUrl = "/site_media/achievements/noimage.jpg"
    return render_to_response('achievements.html', {'achievements':achieved,'noImageUrl':noImageUrl})
