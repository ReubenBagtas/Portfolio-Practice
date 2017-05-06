
from django.conf.urls import url
from . import views           
urlpatterns = [
	url(r'^$', views.index),
	url(r'^register', views.register),
	url(r'^login$', views.login),
	url(r'^quotes$', views.quotes),
	url(r'^quotesprocess$', views.quotesprocess), 
	url(r'^user/(?P<quote_id>\w+)$', views.user),
	url(r'^add$', views.add),
	url(r'^logout$', views.logout),
	url(r'^delete$', views.delete)
]