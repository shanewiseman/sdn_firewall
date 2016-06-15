from django.conf.urls import url

from . import views

urlpatterns = [
        url(r'(?P<token>[0-9A-Fa-f]{64})/v1/(?P<action>ALLOW|DROP|FORWARD)/(?P<address>[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3}.[0-9]{1,3})/$', views.v1FirewallRequest )
]

