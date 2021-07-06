from django.db import models
from django.contrib.auth.models import AbstractUser


class DateInfo(models.Model):
    created_date = models.DateField(auto_now_add=True)
    update_date = models.DateField(auto_now=True)

    class Meta:
        abstract = True


class User(AbstractUser, DateInfo):
    birth = models.DateField(null=True)  # superuser 생성을 위해 null=True
    gender = models.CharField(max_length=10, null=True)  # male / female


class Category(DateInfo):
    category_name = models.CharField(max_length=50, unique=True)


class Brand(DateInfo):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="brands")
    brand_image = models.ImageField()  # imagefield setting.py 추가 설정 필요
    brand_name = models.CharField(max_length=50)
    brand_text = models.TextField()


class Event(DateInfo):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="events")
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name="events")
    event_name = models.CharField(max_length=50)
    event_image = models.ImageField()
    event_banner_image = models.ImageField(null=True)
    event_text = models.TextField(null=True)
    event_due = models.DateField()
    weekly_view = models.DateField()


class Notification(DateInfo):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="notifications")
    notice_type = models.CharField(max_length=10)   # new / finish


class SubscribeBrand(DateInfo):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="subscribebrands")
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name="subscribebrands")


class SubscribeEvent(DateInfo):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="subscribeevents")
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="subscribeevents")
