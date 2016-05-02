from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^update$', views.updateBooking, name='booking-update'),
    url(r'^get/(?P<bookingDate>\d{4}-\d{1,2}-\d{1,2})/$',
        views.sendBookingSlots, name='booking-send'),
]
