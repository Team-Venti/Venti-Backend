from django.contrib import admin

# Register your models here.
from .models import User, Brand, Event, Category, SubscribeBrand, SubscribeEvent, Notification

admin.site.register(User)
admin.site.register(Brand)
# admin.site.register(Event)
admin.site.register(Category)
admin.site.register(SubscribeBrand)
admin.site.register(SubscribeEvent)
admin.site.register(Notification)


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    actions = ['make_notification']

    def make_notification(self, request, queryset):
        for i in queryset:
            subscribe = SubscribeBrand.objects.filter(brand=i.brand.id)
            for j in subscribe:
                Notification.objects.create(user=User.objects.get(id=j.user.id))

    make_notification.short_description = '지정 이벤트의 알림 전송'
