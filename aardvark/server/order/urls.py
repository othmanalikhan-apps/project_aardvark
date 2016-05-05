from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^update$', views.updateOrder, name='order-update'),
]
