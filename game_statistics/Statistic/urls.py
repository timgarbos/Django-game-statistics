from django.conf.urls.defaults import *
urlpatterns = patterns('game_statistics.Statistic.views',
    (r'postentry$', 'postentry'),
    (r'test$', 'test'),
    (r'invite$', 'invite_friends'),
    (r'fbgame/(?P<app_id>\d+)/(?P<stat_name>\w+)/$', 'fb_canvas'),
    (r'$', 'fb_canvas',{'app_id':1,'stat_name':'score'}),
    (r'fbgame/(?P<app_id>\d+)/(?P<stat_name>\w+)/$', 'fb_highscore'),
    

)

