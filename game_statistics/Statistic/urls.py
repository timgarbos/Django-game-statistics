from django.conf.urls.defaults import *
urlpatterns = patterns('game_statistics.Statistic.views',
    (r'^(?P<application_id>\d+)/$', 'postentry'),
    (r'^(?P<application_id>\d+)/test$', 'test'),

)

