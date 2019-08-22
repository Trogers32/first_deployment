from django.conf.urls import url
from . import views
from django.views.generic.base import RedirectView
                    
urlpatterns = [ 
    url(r'^books$', views.home),
    url(r'^books/add$', views.add),
    url(r'^books/add_book$', views.add_book),
    url(r'^users/(?P<num>\d+)$', views.user),
    url(r'^books/(?P<num>\d+)$', views.book),
    url(r'^.*$', RedirectView.as_view(url='/books', permanent=False), name='index')
]