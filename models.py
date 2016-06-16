from __future__ import unicode_literals

from django.db import models


class Token (models.Model):

    token_id = models.CharField(primary_key=True,max_length = 64)
    service  = models.CharField(max_length = 32)

class ForwardEntry (models.Model):

    entry_id = models.CharField(primary_key=True,max_length = 64)
    created  = models.DateTimeField(auto_now=True)

    token = models.ForeignKey(Token, on_delete=models.CASCADE )

    dstaddress  = models.CharField(max_length = 15)
    dstport     = models.CharField(max_length = 13)
    srcaddress   = models.CharField(max_length = 15)
    srcport     = models.CharField(max_length = 13)
    proto       = models.CharField(max_length = 3)
    dsthost     = models.CharField(max_length = 15)


class FirewallEntry ( models.Model ):

    entry_id = models.CharField(primary_key=True,max_length = 64)
    created  = models.DateTimeField(auto_now=True)

    token = models.ForeignKey(Token, on_delete=models.CASCADE )
    forward = models.ForeignKey(ForwardEntry, on_delete=models.CASCADE )

    action   = models.CharField(max_length = 10)

    dstaddress  = models.CharField(max_length = 15)
    dstport     = models.CharField(max_length = 13)
    srcaddress   = models.CharField(max_length = 15)
    srcport     = models.CharField(max_length = 13)
    proto       = models.CharField(max_length = 3)
class TrafficStat (models.Model):

    entry_id = models.CharField(primary_key=True,max_length = 64)
    created  = models.DateTimeField(auto_now=True)
    token = models.ForeignKey(Token, on_delete=models.CASCADE )
    packets  = models.IntegerField()
    bytes  = models.IntegerField()


