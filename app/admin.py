from django.contrib import admin
from .models import User, Flight, Ticket, Seat


admin.site.register(User)
admin.site.register(Flight)
admin.site.register(Ticket)
admin.site.register(Seat)
