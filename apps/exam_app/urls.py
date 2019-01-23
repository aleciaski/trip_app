from django.conf.urls import url
from . import views           # This line is new!
urlpatterns = [
    url(r'^$', views.index),
	url(r'^register$', views.register),
    url(r'^login$', views.login),
    url(r'^success?$', views.success),
    url(r'^add?$', views.add),
    url(r'^createTrip?$', views.createTrip),
    url(r'^createJoin/(?P<trip_id>\d+)$', views.createJoin),
    url(r'^destroyJoin/(?P<trip_id>\d+)$', views.destroyJoin),
     url(r'^show/(?P<trip_id>\d+)$', views.show),
    url(r'^logout$', views.logout),   # This line has changed! Notice that urlpatterns is a list, the comma is in
] 