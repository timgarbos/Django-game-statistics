from django.conf.urls.defaults import *
urlpatterns = patterns('game_statistics.Statistic.views',
    (r'/postentry$', 'postentry'),
    (r'/test$', 'test'),

)

