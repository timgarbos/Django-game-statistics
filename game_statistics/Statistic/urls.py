from django.conf.urls.defaults import *
urlpatterns = patterns('game_statistics.Statistic.views',
    (r'postentry$', 'postentry'),
    (r'test$', 'test'),
    (r'invite$', 'invite_friends'),
    (r'fbgame/(?P<app_id>\d+)/(?P<leaderboard_id>\w+)/$', 'fb_canvas'),
    (r'^$', 'fb_canvas',{'app_id':1,'leaderboard_id':1}),
    (r'highscore/(?P<leaderboard_id>\d+)/$', 'fb_highscore'),
    (r'achievements/(?P<app_id>\d+)/(?P<user_id>\w+)/$', 'achievements'),
    

)

