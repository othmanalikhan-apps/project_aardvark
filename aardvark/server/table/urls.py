from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^total$', views.sendTotalTables, name='table-total'),
]
