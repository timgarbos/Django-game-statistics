from django.db import models
from django.contrib.auth.models import User
from Crypto.PublicKey import RSA
from Crypto import Random
from datetime import datetime

class StatsUser(models.Model):
    def __unicode__(self):
        return self.name
    name = models.CharField(max_length=300)
    uid = models.IntegerField(null=True, blank=True)
    type = models.CharField(max_length=300)
    created_date = models.DateTimeField(default=datetime.now)
    def update_acheivements(self,app_id):
        achievements = Achievement.objects.filter(application__id=app_id)
        for a in achievements:
            if a.comparator == 'GT':
                values = StatisticEntry.objects.filter(statistic__id=a.statistic.id).order_by('-value')
                if values.count() > 0:
                    value = values[0]
                    if value>a.value:
                        ua, created = UserAchievement.objects.get_or_create(achievement=a,user=self)
                        if created:
                            ua.save()
            else:
                values = StatisticEntry.objects.filter(statistic__id=a.statistic.id).order_by('value')
                if values.count() > 0:
                    value = values[0]
                    if value<a.value:
                        ua, created = UserAchievement.objects.get_or_create(achievement=a,user=self)
                        if created:
                            ua.save()

            

class Application(models.Model):
    def __unicode__(self):
        return self.name
    name = models.CharField(max_length=300)
    owners = models.ManyToManyField(User)
    private_key = models.CharField(max_length=1024,blank=True)
    public_key = models.CharField(max_length=1024,blank=True)
    created_date = models.DateTimeField(default=datetime.now)
    def save(self, *args, **kwargs):
        if self.private_key == "" or self.public_key == "":
            #Generate private/public key pairs
            r = Random.new()
            key = RSA.generate(1024, r.read)
            pub = key.publickey()
            self.private_key = key.exportKey()
            self.public_key = pub.exportKey()
        super(Application, self).save(*args, **kwargs) # Call the "real" save() method.
    
    
class StatisticType(models.Model):
    def __unicode__(self):
        return self.name
    name = models.CharField(max_length=300)
    created_date = models.DateTimeField(default=datetime.now)
    
class Statistic(models.Model):
    def __unicode__(self):
        return self.name
    name = models.CharField(max_length=300)
    application = models.ForeignKey(Application)
    type = models.ForeignKey(StatisticType,null=True)
    created_date = models.DateTimeField(default=datetime.now)

    
class StatisticEntry(models.Model):
    def __unicode__(self):
        return str(self.value)
    value = models.IntegerField()
    statistic = models.ForeignKey(Statistic)
    user = models.ForeignKey(StatsUser)
    pub_date = models.DateTimeField(default=datetime.now)
    build_version = models.IntegerField()
    game_session = models.IntegerField()
    

class LeaderBoard(models.Model):
    def __unicode__(self):
        return self.name
    statistic = models.ForeignKey(Statistic)
    weekly = models.BooleanField()
    name = models.CharField(max_length=300)
    created_date = models.DateTimeField(default=datetime.now)


COMPARATOR_CHOICES = (
    ('GT', 'Greater Than'),
    ('LT', 'Less Than'),
    ('EQ', 'Equals'),
)

class Achievement(models.Model):
    def __unicode__(self):
        return self.name
    statistic = models.ForeignKey(Statistic)
    application = models.ForeignKey(Application)
    value = models.IntegerField()
    index = models.IntegerField() #Used for Open Feint
    image = models.ImageField(upload_to='achievements', null=True, blank=True)
    #image_thumb = models.ImageField(upload_to='achievements/thumbs', null=True, blank=True)
    name = models.CharField(max_length=300)
    description = models.TextField()
    created_date = models.DateTimeField(default=datetime.now)
    comparator = models.CharField(max_length=2, choices=COMPARATOR_CHOICES)

class UserAchievement(models.Model):
    def __unicode__(self):
        return self.achievement.name
    achievement = models.ForeignKey(Achievement)
    pub_date = models.DateTimeField(default=datetime.now)
    user = models.ForeignKey(StatsUser)
