# coding=utf-8
from django.contrib import admin
from background_task import background
from .models import *
from datetime import datetime, timedelta

# Register your models here.
from .models import User, Brand, Event, Category, SubscribeBrand, SubscribeEvent, Notification

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
    list_display = ['id', 'name', 'category', 'view']
    list_display_links = ['id', 'name']
    actions = ['make_banner']

    def make_banner(self, request, queryset):
        for each in queryset:
            Banner.objects.create(name=each.name, brand_id=each.id, view=each.view)

    make_banner.short_description = '지정 브랜드 배너 생성'


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'category', 'brand', 'due', 'view']
    list_display_links = ['id', 'name']
    actions = ['make_notification']

    def make_notification(self, request, queryset):
        for i in queryset:
            subscribe = SubscribeBrand.objects.filter(brand=i.brand.id)
            for j in subscribe:
                user = User.objects.filter(id=j.user.id)
                user.update(noti_state=True)
                Notification.objects.create(user=User.objects.get(id=j.user.id), brand=i.brand, event=Event.objects.get(name=i.name), notice_type="new")

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
    actions = ['noti']

    def noti(self, request, queryset):
        noti_bg(repeat=3600)

    noti.short_description = '마감알람 시작하기'


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'brand_id', 'view']
    list_display_links = ['id', 'name']


@background(schedule=3600)
def noti_bg():
    # 현재 시간 가져오기
    now = datetime.now().strftime('%Y-%m-%d %h:%m:%s')
    # 12시간 전
    now12 = datetime.now() + timedelta(hours=12)
    now24 = datetime.now() + timedelta(hours=24)
    now48 = datetime.now() + timedelta(hours=48)
    # 12시간 전 이벤트들
    endevent12 = Event.objects.filter(due__gte=(now12 - timedelta(minutes=30)), due__lte=(now12 + timedelta(minutes=29)))
    endevent24 = Event.objects.filter(due__gte=(now24 - timedelta(minutes=30)), due__lte=(now24 + timedelta(minutes=29)))
    endevent48 = Event.objects.filter(due__gte=(now48 - timedelta(minutes=30)), due__lte=(now48 + timedelta(minutes=29)))

    # 이 이벤트를 좋아하는 유저 찾기
    if endevent12.count() != 0:
        for i in endevent12:
            likeevents = SubscribeEvent.objects.filter(event=i.id)
            for j in likeevents:
                user = User.objects.filter(id=j.user.id)
                user.update(noti_state=True)
                Notification.objects.create(user=j.user, event=i, brand=i.brand, notice_type="end12")
    # 이 이벤트를 좋아하는 유저 찾기
    if endevent24.count() != 0:
        for i in endevent24:
            likeevents = SubscribeEvent.objects.filter(event=i.id)
            for j in likeevents:
                user = User.objects.filter(id=j.user.id)
                user.update(noti_state=True)
                Notification.objects.create(user=j.user, event=i, brand=i.brand, notice_type="end24")
    # 이 이벤트를 좋아하는 유저 찾기
    if endevent48.count() != 0:
        for i in endevent48:
            likeevents = SubscribeEvent.objects.filter(event=i.id)
            for j in likeevents:
                user = User.objects.filter(id=j.user.id)
                user.update(noti_state=True)
                Notification.objects.create(user=j.user, event=i, brand=i.brand, notice_type="end48")
