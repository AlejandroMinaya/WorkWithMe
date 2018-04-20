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

    def isOwner(self, owner):
        if owner == self.projectOwner:
            return True
        return False

class Task(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    project = models.ForeignKey(Project, on_delete = models.CASCADE)
    creationDate = models.DateField(auto_now_add=True)
    # state = -1 means that the projec is just created
    # state = 0 means that the project is ready to revision
    # state = 1 means that the project is compleated
    state = models.IntegerField(default=-1)
    dueDate = models.DateField()
    responsible = models.ForeignKey(User, on_delete = models.CASCADE)


    def addResponsible(user):
        responsible = user
        return True

    def modifyState(newState):
        state = newState
        return
