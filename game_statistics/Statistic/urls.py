from django.conf.urls.defaults import *
urlpatterns = patterns('game_statistics.Statistic.views',
    (r'postentry$', 'postentry'),
    (r'test$', 'test'),
    (r'fbgame/^(?P<app_id>\d+)/(?P<stat_name>\w+)$', 'fb_canvas'),

)

