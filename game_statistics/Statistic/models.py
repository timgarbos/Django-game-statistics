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

class Application(models.Model):
    def __unicode__(self):
        return self.name
    name = models.CharField(max_length=300)
    owners = models.ManyToManyField(User)
    private_key = models.CharField(max_length=1024,blank=True)
    public_key = models.CharField(max_length=1024,blank=True)
    
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
    
class Statistic(models.Model):
    def __unicode__(self):
        return self.name
    name = models.CharField(max_length=300)
    application = models.ForeignKey(Application)
    type = models.ForeignKey(StatisticType)
    isPublic = models.BooleanField()

    
class StatisticEntry(models.Model):
    def __unicode__(self):
        return str(self.value)
    value = models.IntegerField()
    statistic = models.ForeignKey(Statistic)
    user = models.ForeignKey(StatsUser)
    pub_date = models.DateTimeField(default=datetime.now)
    

