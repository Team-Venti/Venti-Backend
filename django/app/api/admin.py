from django.contrib import admin

# Register your models here.
from .models import User, Brand, Event

admin.site.register(User)
admin.site.register(Brand)
admin.site.register(Event)