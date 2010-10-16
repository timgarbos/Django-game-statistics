from game_statistics.Statistic.models import *

from django.contrib import admin




admin.site.register(Application)
admin.site.register(StatisticType)
admin.site.register(Statistic)
admin.site.register(StatisticEntry)
admin.site.register(StatsUser)
