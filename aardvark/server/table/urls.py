from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^update$', views.updateBooking, name='booking-update'),
    url(r'^get$', views.sendBookingSlots, name='booking-send'),
]
