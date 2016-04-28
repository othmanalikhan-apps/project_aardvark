from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^get$', views.sendMenu, name='menu-get'),
    url(r'^update$', views.updateMenu, name='menu-update'),
]
