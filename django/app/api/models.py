from django.db import models
from django.contrib.auth.models import AbstractUser


class DateInfo(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class User(AbstractUser, DateInfo):
    birth = models.DateField(null=True)
    gender = models.CharField(max_length=10, blank=True)  # male / female
    nickname = models.CharField(max_length=20, unique=True)
    noti_state = models.BooleanField(default=False)


class Category(DateInfo):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):  # admin 페이지 출력
        return self.name


class Brand(DateInfo):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="brands")
    image = models.ImageField(null=True, upload_to="brand_logo")
    banner_image = models.ImageField(null=True, upload_to="brand_banner")
    name = models.CharField(max_length=50)
    text = models.TextField(null=True)
    view = models.IntegerField(null=True, default=0)

    def __str__(self):
        return self.name


class Event(DateInfo):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="events")
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name="events")
    name = models.CharField(max_length=50)
    image = models.ImageField(null=True, upload_to="event_logo")
    text = models.TextField(null=True)
    due = models.DateTimeField(null=True)
    view = models.IntegerField(null=True, default=0)
    url = models.URLField(null=True)
    ocr_text = models.TextField(null=True)

    def __str__(self):
        return self.name


class Notification(DateInfo):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="notifications")
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name="notifications")
    notice_type = models.CharField(max_length=10)  # new / end

    def __str__(self):
        return str(self.user.username) + "의 " + str(self.event) + " 이벤트 알림"


class SubscribeBrand(DateInfo):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="subscribebrands")
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, related_name="subscribebrands")

    def __str__(self):
        return str(self.user.username) + "의 " + str(self.brand) + " 브랜드 구독"


class SubscribeEvent(DateInfo):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="subscribeevents")
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="subscribeevents")

    def __str__(self):
        return str(self.user.username) + "의 " + str(self.event) + " 이벤트 좋아요"


class Banner(DateInfo):
    name = models.CharField(max_length=50)
    brand_id = models.IntegerField()
    view = models.IntegerField(default=0)

