from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Message(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.CharField(max_length=150)
    time_stamp = models.DateTimeField(auto_now_add=True)
    room_name = models.CharField(max_length=50, null=True)

    def __str__(self):
        return self.author.username

    # get 10 most recent messages

    @staticmethod
    def get_most_recent_messages(room_name):
        return Message.objects.filter(room_name=room_name).order_by('time_stamp')[:15]


