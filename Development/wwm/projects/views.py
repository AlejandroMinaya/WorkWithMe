from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from users.models import User
from datetime import date
from django.views.decorators.csrf import csrf_exempt
from .models import Project, Task, RecentActivity

EMPTY_REQUEST_MSSG = "Empty Request"
PROJECT_NOT_FOUND_MSSG = "Project not found"
TASK_NOT_FOUND_MSSG = "Task not found" 
USER_NOT_FOUND_MSSG = "User not found"
PERMISSION_DENIED_MSSG = "This user is not the owner of the project"

# IMPORTANT !!!!#
# Most of the methods at the end will have to create a RecentActivity object
# to keep historical record of what has been done
#
# Also, we need the award system to be in place

    

# Create your views here.

# HTML PAGES
# =====================================================
def index(request):
    template = loader('index.html')
    context = {}
    return HttpResponse("index")


# GENERAL MANAGEMENT METHODS
# =====================================================
# - PRIVATE METHODS
# -----------------------------------------------------
# -- GET A USER
# Retrieves an user from the database using its ID/PK
def getUser(userID):
    try:
        return User.objects.get(id=userID)
    except:
        return None

# -- VERIFY EXISTENCE
def verifyExistence(**kwargs):
    if "user" in kwargs:
        for user in kwargs["user"]:
            if user == None:
                return HttpResponse(USER_NOT_FOUND_MSSG)
    if "task" in kwargs:
        if kwargs["task"] == None:
            return HttpResponse(TASK_NOT_FOUND_MSSG)
    if "project" in kwargs:
        if kwargs["project"] == None:
            return HttpResponse(PROJECT_NOT_FOUND_MSSG)
    return True


# PROJECT MANAGMENT METHODS
# =====================================================

# - PRIVATE METHODS
# -----------------------------------------------------
# -- GET A PROJECT
# Retrieves a project from the database using its ID/PK
def getProject(projectID):
    try:
       return Project.objects.get(id=projectID)
    except:
        return None

# -- CREATE RECENT ACTIVITY LOG
# Creates a record of the action performed for future reference
def createRecentActivity(**kwargs):
    tmp = RecentActivity()
    if "triggerActor" in kwargs:
        tmp.triggerActor = kwargs["triggerActor"]
    if "targetActor" in kwargs:
        tmp.targetActor = kwargs["targetActor"]
    if "project" in kwargs:
        tmp.project = kwargs["project"]
    if "task" in kwargs:
        tmp.task = kwargs["task"]
    if "action" in kwargs:
        tmp.action = kwargs["action"]
    tmp.save()


# - FORM METHODS
# -----------------------------------------------------
# -- ADD A PROJECT
# Adds a new project setting the session user as the owner
#
# Needs the POST arguments:
#   (Project)
#   > name
#   > dueYear
#   > dueMonth
#   > dueDay
@csrf_exempt
def add(request):
    if request.method == 'POST':
        user = getUser(request.session["userID"])
        verification = verifyExistence(user=[user])
        if type(verification) == HttpResponse:
            return verification
        _name = request.POST["name"]
        _dueDate = date(int(request.POST["dueYear"]), int(request.POST["dueMonth"]), int(request.POST["dueDay"]))  
        _projectOwner = user
        newProject = Project(name=_name, projectOwner=_projectOwner, dueDate=_dueDate)
        newProject.save()
        newProject.members.add(_projectOwner)
        newProject.save()
        createRecentActivity(triggerActor=user, project=newProject, action=RecentActivity.ADD_PROJECT)
        return HttpResponse("Project created")
    return HttpResponse(EMPTY_REQUEST_MSSG)

# -- EDIT PROJECT
# Edits a project's information
#
# Needs the POST arguments:
#   > 
def edit(request):
    return HttpResponse("hola")

# -- DELETE A PROJECT
# Deletes a project if the session user is the owner of said project
#
# Needs the POST arguments:
#   > projectID
@csrf_exempt
def delete(request):
    if request.method == 'POST':
        project = getProject(request.POST["projectID"])
        user = getUser(request.session["userID"])
        verification = verifyExistence(user=[user], project=project)
        if type(verification) == HttpResponse:
            return verification
        if user == project.projectOwner:
            project.delete()
            createRecentActivity(triggerActor=user, project=project, action=RecentActivity.REMOVE_PROJECT)
            return HttpResponse("Project deleted")
        return HttpREsponse(PERMISSION_DENIED_MSSG)
    return HttpResponse(EMPTY_REQUEST_MSSG)

# -- LEAVE A PROJECT
# Leave a project^
# ^If the leaving user is the owner, the ownership is transferred to another project  member
#
# Needs the POST arguments:
#   > projectID
@csrf_exempt
def leave(request):
    if request.method == 'POST':
        newOwnerFound = False
        project = getProject(request.POST["projectID"])
        user = getUser(request.session["userID"])
        verification = verifyExistence(user=[user], project=project)
        if type(verification) == HttpResponse:
            return verification
        if user == project.projectOwner:
            for member in project.members.all():
                if member != user:
                    project.projectOwner = member
                    newOwnerFound = True
                    break
            if not newOwnerFound:
                # Should the project be deleted if the owner left?

                # PROJECT DELETION
                #project.delete()
                #return HttpResponse("Project deleted")
                pass
        project.members.remove(user)
        project.save()
        createRecentActivity(triggerActor=user, project=project, action=RecentActivity.LEAVE_PROJECT)
        return HttpResponse("User removed from group")
    return HttpResponse(EMPTY_REQUEST_MSSG)

# -- ADD MEMBER TO PROJECT
# Adds a new member to a project by one of the members.
#
# Needs the POST arguments:
#   > userID - Member to be added
#   > projectID
@csrf_exempt
def addMember(request):
    if request.method == 'POST':
        newMember = getUser(request.POST["userID"])
        user = getUser(request.session["userID"])
        project = getProject(request.POST["projectID"])
        verification = verifyExistence(user=[user, newMember], project=project)
        if type(verification) == HttpResponse:
            return verification
        if user in project.members.all():
            project.members.add(newMember)
            createRecentActivity(triggerActor=user, targetActor=newMember, project=project, action=RecentActivity.ADD_MEMBER)
            return HttpResponse("User added to group")
        return HttpResponse(PERMISSION_DENIED_MSSG)
    return HttpResponse(EMPTY_REQUEST_MSSG)

# -- REMOVE MEMBER TO PROJECT
# Removes a member from a project by the project owner.
#
# Needs the POST arguments:
#   > userID - Member to be removed
#   > projectID
@csrf_exempt
def removeMember(request):
    if request.method == 'POST':
        user = getUser(request.session["userID"])
        removedMember = getUser(request.POST["userID"])
        project = getProject(request.POST["projectID"])
        verification = verifyExistence(user=[user, removedMember], project=project)
        if type(verification) == HttpResponse:
            return verification
        if user == project.projectOwner:
            project.members.remove(removedMember)
            createRecentActivity(triggerActor=user, targetActor=newMember, project=project, action=RecentActivity.REMOVE_MEMBER)
            return HttpResponse("User removed")
        return HttpResponse(PERMISSION_DENIED_MSSG)
    return HttpResponse(EMPTY_REQUEST_MSSG)


# TASK MANAGEMENT METHODS
# =====================================================
# - PRIVATE METHODS
# -----------------------------------------------------
# -- GET A TASK
# Retrieves a task based on a ID/PK
def getTask(taskID):
    try:
        return Task.objects.get(id=taskID)
    except:
        return None

# - FORM METHODS
# -----------------------------------------------------
# -- ADD A TASK
# Add a new task to a project by one of its members
#
# Needs the POST arguments:
#   > projectID
# 
#  (Task)
#   > name
#   > description
#   > dueYear
#   > dueMonth
#   > dueDay
#   > responsibleID
@csrf_exempt
def addTask(request):
    if request.method == 'POST':
        project = getProject(request.POST["projectID"])
        user = getUser(request.session["userID"])
        verification = verifyExistence(user=[user], project=project)
        if type(verification) == HttpResponse:
            return verification
        if user in project.members.all():
            task = Task()
            task.name = request.POST["name"]
            task.description = request.POST["description"]
            task.project = project
            task.dueDate = date(int(request.POST["dueYear"]), int(request.POST["dueMonth"]), int(request.POST["dueDay"]))
            responsible = getUser(request.POST["responsibleID"])
            if responsible == None or responsible not in project.members.all():
                responsible = user
            task.responsible = responsible
            task.save()
            createRecentActivity(triggerActor=user, targetActor=responsible, project=project, task=task, action=RecentActivity.ASSIGN_TASK)
            return HttpResponse("Task added")
        return HttpResponse(PERMISSION_DENIED_MSSG)
    return HttpResponse(EMPTY_REQUEST_MSSG)


# -- EDIT A TASK


# -- REMOVE A TASK
# Remove a task by the project owner or task responsible
#
# Needs the POST arguments
#   > taskID
@csrf_exempt
def removeTask(request):
    if request.method == 'POST':
        user = getUser(request.session["userID"])
        task = getTask(request.POST["taskID"])
        verification = verifyExistence(user=[user], task=task)
        if type(verification) == HttpResponse:
            return verification
        if user == task.project.projectOwner or user == task.responsible:
            task.delete()
            createRecentActivity(triggerActor=user, project=project, task=task, action=RecentActivity.REMOVE_TASK)
            return HttpResponse("Task deleted")
        return HttpResponse(PERMISSION_DENIED_MSSG)
    return HttpResponse(EMPTY_REQUEST_MSSG)

# -- MARK A TASK FOR VERIFICATION
# Marks a task for verification by one of the team members
#
# Needs the POST argumets
#   > taskID
@csrf_exempt
def markTaskForVerification(request):
    if request.method == 'POST':
        user = getUser(request.session["userID"])
        task = getTask(request.POST["taskID"])
        verification = verifyExistence(user=[user], task=task)
        if type(verification) == HttpResponse:
            return verification
        if user != task.responsible and user != task.project.projectOwner:
            return HttpResponse(PERMISSION_DENIED_MSSG)
        successMssg = ""
        if user == task.responsible:
            task.status = 0
            successMssg = "Task marked for verification"
            createRecentActivity(triggerActor=user, project=project, task=task, action=RecentActivity.MARK_TASK)
        if user == task.project.projectOwner:
            task.status = 1
            successMssg = "Task completed"
            createRecentActivity(triggerActor=user, project=project, task=task, action=RecentActivity.COMPLETE_TASK)
        task.save()
        return HttpResponse(successMssg)
    return HttpResponse(EMPTY_REQUEST_MSSG)

# -- VERIFY A TASK
# Verify a task by a team member other than the responsible
#
# Needs the POST argumets
#   > taskID
@csrf_exempt
def verifyTask(request):
    if request.method == 'POST':
        user = getUser(request.session["userID"])
        task = getTask(request.POST["taskID"])
        reject = bool(int(request.POST["reject"]))
        verification = verifyExistence(user=[user], task=task)
        if type(verification) == HttpResponse:
            return verification
        if user != task.responsible and user in task.project.members.all():
            successMssg = ""
            if reject:
                task.status = 1
                successMssg = "Task completed"
                createRecentActivity(triggerActor=user, project=project, task=task, action=RecentActivity.COMPLETE_TASK)
            else:
                task.status = -1
                successMssg = "Task rejected"
                createRecentActivity(triggerActor=user, project=project, task=task, action=RecentActivity.REJECT_TASK)
            task.save()
            return HttpResponse(successMssg)
        return HttpResponse(PERMISSION_DENIED_MSSG)
    return HttpResponse(EMPTY_REQUEST_MSSG)

# -- CHANGE TASK RESPONSIBLE
# Change the responsible member to a task 
#
# Needs the POST argumets
#   > taskID
#   > userID - new responsible
@csrf_exempt
def changeTaskResponsible(request):
    if request.method == 'POST':
        newResponsible = getUser(request.POST["userID"])
        user = getUser(request.session["userID"])
        task = getTask(request.POST["taskID"])
        verification = verifyExistence(user=[user, newResponsible], task=task)
        if type(verification) == HttpResponse:
            return verification
        if user == task.project.projectOwner:
            task.responsible = newResponsible
            task.save()
        return HttpResponse(PERMISSION_DENIED_MSSG)
    return HttpResponse(EMPTY_REQUEST_MSSG)

# -- REMOVE RESPONSIBLE FROM TASK
