from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.
class File(models.Model):
    docname = models.CharField(max_length=100, blank=True)
    docintro = models.CharField(max_length=300, blank=True)
    doctitle = models.CharField(max_length=100, blank=True)
    doctext = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="files")
    createtime = models.DateTimeField(default=timezone.now)
    lasttime = models.DateTimeField(auto_now=True)
    # lastauthor = models.ForeignKey(Group, on_delete=models.CASCADE)
    # group = ForeignKey()
    stat = models.IntegerField(default=0)
    admindoc = models.IntegerField(default=0)
    deletetime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.doctitle


class CollectList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="collected")
    file = models.ForeignKey(File, on_delete=models.CASCADE)

    def __str__(self):
        return self.user
