from __future__ import unicode_literals

from django.db import models


class Token (models.Model):

    token_id = models.CharField(primary_key=True,max_length = 64)
    service  = models.CharField(max_length = 32)

class FirewallEntry ( models.Model ):

    entry_id = models.CharField(primary_key=True,max_length = 64)
    created  = models.DateTimeField()
    token_id = models.ForeignKey(Token, on_delete=models.CASCADE )
    address  = models.CharField(max_length = 15)
    action   = models.CharField(max_length = 10)
    options  = models.CharField(max_length = 255)

class ForwardEntry (models.Model):

    entry_id = models.CharField(primary_key=True,max_length = 64)
    created  = models.DateTimeField()
    token_id = models.ForeignKey(Token, on_delete=models.CASCADE )
    address  = models.CharField(max_length = 15)
    options  = models.CharField(max_length = 255)
    SNAT     = models.BooleanField

class TrafficStat (models.Model):

    entry_id = models.CharField(primary_key=True,max_length = 64)
    created  = models.DateTimeField()
    token_id = models.ForeignKey(Token, on_delete=models.CASCADE )
    packets  = models.IntegerField()
    bytes  = models.IntegerField()


