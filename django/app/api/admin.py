from django.contrib import admin

# Register your models here.
from .models import User, Brand, Event, Category, SubscribeBrand, SubscribeEvent, Notification, Banner

# admin.site.register(User)
# admin.site.register(Brand)
# admin.site.register(Event)
# admin.site.register(Category)
# admin.site.register(SubscribeBrand)
# admin.site.register(SubscribeEvent)
# admin.site.register(Notification)
# admin.site.register(Banner)


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ['id', 'username', 'is_superuser', 'is_staff']
    list_display_links = ['id', 'username']


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'category']
    list_display_links = ['id', 'name']
    actions = ['make_banner_brand']

    def make_banner_brand(self, request, queryset):
        for i in queryset:
            Banner.objects.create(name=i.name, count=0)

    make_banner_brand.short_description = '지정 브랜드의 배너 브랜드 추가'


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'category', 'brand', 'due', 'view']
    list_display_links = ['id', 'name']
    actions = ['make_notification']

    def make_notification(self, request, queryset):
        for i in queryset:
            subscribe = SubscribeBrand.objects.filter(brand=i.brand.id)
            for j in subscribe:
                Notification.objects.create(user=User.objects.get(id=j.user.id), event=Event.objects.get(name=i.name), notice_type="new")

    make_notification.short_description = '지정 이벤트의 알림 전송'


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_display_links = ['id', 'name']


@admin.register(SubscribeBrand)
class SubscribeBrandAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'brand']
    list_display_links = ['id', 'user']


@admin.register(SubscribeEvent)
class SubscribeEventAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'event']
    list_display_links = ['id', 'user']


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'event', 'notice_type', 'brand']
    list_display_links = ['id', 'user']


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'count']
    list_display_links = ['id', 'name']