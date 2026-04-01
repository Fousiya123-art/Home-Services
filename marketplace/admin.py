from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(ServiceCategory)
admin.site.register(ServiceProvider)
admin.site.register(Service)
admin.site.register(Booking)
admin.site.register(Review)
admin.site.register(cart)
admin.site.register(profile)
admin.site.register(QuoteRequest)
admin.site.register(ContactMessage)
