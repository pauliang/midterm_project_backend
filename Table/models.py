from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


# Create your models here.
class File(models.Model):
    docname = models.CharField(max_length=100, blank=True)
    docintro = models.CharField(max_length=300, blank=True, null=True)
    doctitle = models.CharField(max_length=100, blank=True, null=True)
    doctext = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="files")
    createtime = models.DateTimeField(default=timezone.now)
    lasttime = models.DateTimeField(auto_now=True)
    # lastauthor = models.ForeignKey(Group, on_delete=models.CASCADE)
    # group = ForeignKey()
    stat = models.IntegerField(default=0)
    admindoc = models.IntegerField(default=0)
    deletetime = models.DateTimeField(blank=True, null=True)
    lastauthor = models.ForeignKey(User, on_delete=models.CASCADE)
    isedit = models.IntegerField(default=1)
    groupnum = models.IntegerField(default=-1)

    @classmethod
    def new_file(cls, docname, content, author):
        file = cls(docname=docname, doctitle=docname, doctext=content, author=author, lastauthor=author)
        return file

    def __str__(self):
        return self.docname


class CollectList(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="collected")
    file = models.ForeignKey(File, on_delete=models.CASCADE)

    def __str__(self):
        return self.user
