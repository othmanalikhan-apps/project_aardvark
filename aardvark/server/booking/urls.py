from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^update$', views.updateBooking, name='booking-update'),
    url(r'^sizes$', views.sendBookingSizes, name='booking-sizes'),
    url(r'^tables$', views.sendBookingTables, name='booking-tables'),
]
