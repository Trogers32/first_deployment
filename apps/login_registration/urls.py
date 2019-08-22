from django.conf.urls import url
from . import views
                    
urlpatterns = [
    url(r'^$', views.home),
    url(r'^user$', views.login),
    url(r'^logout$', views.logout),
    url(r'^success$', views.success),
    url(r'^register$', views.register),
]