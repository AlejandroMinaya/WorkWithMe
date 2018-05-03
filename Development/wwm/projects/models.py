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

    def getIntProgress(self):
        return int(self.progress)


class Task(models.Model):
    name = models.CharField(max_length=255)
    description = models.CharField(max_length=255)
    project = models.ForeignKey(Project, on_delete = models.CASCADE)
    creationDate = models.DateTimeField(auto_now_add=True)
    # status = -1 means that the projec is just created
    # status = 0 means that the project is ready to revision
    # status = 1 means that the project is compleated
    status = models.IntegerField(default=-1)
    dueDate = models.DateField()
    responsible = models.ForeignKey(User, on_delete = models.CASCADE)

class RecentActivity(models.Model):
    ADD_TASK = "%s added a new task to %s."
    MARK_TASK = "%s marked %s for revision. <a href='/project/%s'>Check it out!</a>"
    COMPLETE_TASK = "%s just verified <a href='/project/%s'>%s</a>. Congrats on the progress!"
    REMOVE_TASK = "%s deleted %s."
    REMOVE_PROJECT = "%s deleted the %s project."
    ADD_PROJECT = "%s created %s. <a href='/project/%s'>Let's go</a>"
    LEAVE_PROJECT = "%s had to leave %s. Farewell"
    ADD_MEMBER = "%s joined %s. <a href='/project/%s'>Get started!</a>"
    REMOVE_MEMBER = "%s was asked to leave %s. Until the next one"
    ASSIGN_TASK = "%s assigned %s to %s. <a href='/project/%s'>Give it a look...</a>"
    REJECT_TASK = "%s rejected <a href='/project/%s'>%s</a>."
    UNMARK_TASK = "%s unmarked %s. <a href='/project/%s'>Check it out!</a>"
    triggerActor = models.ForeignKey(User, on_delete = models.CASCADE, related_name="triggerActor")
    targetActor = models.ForeignKey(User, on_delete = models.CASCADE, null=True, related_name="targetActor")
    timestamp = models.DateTimeField(auto_now_add=True)
    action = models.CharField(default=" ", max_length=1000)
    task = models.ForeignKey(Task, on_delete = models.CASCADE, null=True)
    project = models.ForeignKey(Project, on_delete = models.CASCADE, null=True)

    def getMessage(self):
        mssg = self.action
        if (mssg == self.ADD_TASK or mssg == self.REMOVE_TASK):
            return mssg % (self.triggerActor.firstName, self.task.name)
        if(mssg == self.MARK_TASK or mssg == self.COMPLETE_TASK or mssg == self.REJECT_TASK or mssg == self.UNMARK_TASK):
            return mssg % (self.triggerActor.firstName, self.task.name, self.project.id)
        if(mssg == self.REMOVE_PROJECT or mssg == self.LEAVE_PROJECT):
            return mssg % (self.triggerActor.firstName, self.project.name)
        if(mssg == self.ADD_PROJECT):
            return mssg % (self.triggerActor.firstName, self.project.name, self.project.id)
        if(mssg == self.REMOVE_MEMBER):
            return mssg % (self.targetActor.firstName, self.project.name)
        if(mssg == self.ADD_MEMBER):
            return mssg % (self.targetActor.firstName, self.project.name, self.project.id)
        if(mssg == self.ASSIGN_TASK):
            return mssg % (self.triggerActor.firstName, self.targetActor.firstName, self.task.name, self.project.id)
                
