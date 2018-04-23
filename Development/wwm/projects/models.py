from django.db import models
from users.models import User
from datetime import date

# Create your models here.
class Project(models.Model):
    name = models.CharField(max_length=255)
    #description = models.CharField(max_length=500)
    progress = models.FloatField(default=0)
    members = models.ManyToManyField(User)
    projectOwner = models.ForeignKey(User, on_delete= models.CASCADE, related_name="ProjectOwner")
    dueDate = models.DateField(default=date(1999, 1, 21))


class Task(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    project = models.ForeignKey(Project, on_delete = models.CASCADE)
    creationDate = models.DateField(auto_now_add=True)
    # status = -1 means that the projec is just created
    # status = 0 means that the project is ready to revision
    # status = 1 means that the project is compleated
    status = models.IntegerField(default=-1)
    dueDate = models.DateField()
    responsible = models.ForeignKey(User, on_delete = models.CASCADE)

