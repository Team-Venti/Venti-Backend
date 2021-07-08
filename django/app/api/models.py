from django.db import models
from django.contrib.auth.models import AbstractUser


class DateInfo(models.Model):
    created_date = models.DateField(auto_now_add=True)
    update_date = models.DateField(auto_now=True)

    class Meta:
        abstract = True


class User(AbstractUser, DateInfo):
    birth = models.DateField(null=True)
    gender = models.CharField(max_length=10, null=True)  # male / female


class Category(DateInfo):
    name = models.CharField(max_length=50, unique=True)


class Brand(DateInfo):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="brands")
    image = models.ImageField()  # imagefield setting.py 추가 설정 필요
    name = models.CharField(max_length=50)
    text = models.TextField(null=True)


class Event(DateInfo):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="events")
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name="events")
    name = models.CharField(max_length=50)
    image = models.ImageField(null=True)
    banner_image = models.ImageField(null=True)
    text = models.TextField(null=True)
    due = models.DateField(null=True)
    weekly_view = models.DateField(default=0, null=True)
    url = models.URLField(null=True)


class Notification(DateInfo):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="notifications")
    notice_type = models.CharField(max_length=10)   # new / end


class SubscribeBrand(DateInfo):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="subscribebrands")
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name="subscribebrands")


class SubscribeEvent(DateInfo):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="subscribeevents")
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="subscribeevents")
