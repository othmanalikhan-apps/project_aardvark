from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^update$', views.updateOrder, name='order-update'),
    url(r'^bill$', views.calculateBill, name='order-bill'),
    url(r'^payment$', views.updateBill, name='order-payment'),
]
