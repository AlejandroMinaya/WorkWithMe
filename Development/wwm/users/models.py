from django.db import models

# Create your models here.
class Permission(models.Model):
    name = models.CharField(max_length=255, null=True)
    description = models.CharField(max_length=500, null=True)

class Role(models.Model):
    name = models.CharField(max_length=255, null=True)
    description = models.CharField(max_length=255, null=True)
    permission = models.ManyToManyField(Permission)

class User(models.Model):
    firstName = models.CharField(max_length=255, null=True)
    lastName = models.CharField(max_length=255, null=True)
    email = models.EmailField(max_length=254, null=True)
    rating = models.FloatField(null=True)
    level = models.IntegerField(null=True)
    role = models.ForeignKey(Role, on_delete=models.CASCADE, related_name="+", null=True)

    def __str__(self):
        string = "USER: "+ self.firstName+" "+self.lastName+"\n"
        string += "E-mail: " + self.email + "\n"
        string += "Rating: " + str(self.rating) + "\n"
        string += "Level: " + str(self.level) + "\n"
        string += "Role: " + str(self.role) + "\n"
        return string



