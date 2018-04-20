from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from users.models import User
from datetime import date
from django.views.decorators.csrf import csrf_exempt
from .models import Project

EMPTY_REQUEST_MSSG = "Empty Request"
PROJECT_NOT_FOUND_MSSG = "Project with id %s not found AND/OR User with id %s not found"
USER_NOT_FOUND_MSSG = "User with id %s not found"
PERMISSION_DENIED_MSSG = "This user is not the owner of the project"


    

# Create your views here.
def index(request):
    # Dashboard
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
        if user == None:
            return HttpResponse(USER_NOT_FOUND_MSSG % request.session["userID"])
        _name = request.POST["name"]
        _dueDate = date(int(request.POST["dueYear"]), int(request.POST["dueMonth"]), int(request.POST["dueDay"]))  
        _projectOwner = user
        newProject = Project(name=_name, projectOwner=_projectOwner, dueDate=_dueDate)
        newProject.save()
        newProject.members.add(_projectOwner)
        newProject.save()
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
        user = getuser(request.session["userID"])
        if user == None:
            return HttpResponse(USER_NOT_FOUND_MSSG % request.session["userID"])
        if project == None:
            return HttpResponse(PROJECT_NOT_FOUND_MSSG  % request.POST["projectID"])
        if user == project.projectOwner:
            project.delete()
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
        if user == None:
            return HttpResponse(USER_NOT_FOUND_MSSG % request.session["userID"])
        if project == None:
            return HttpResponse(PROJECT_NOT_FOUND_MSSG % request.POST["projectID"])
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
        if newMember == None:
            return HttpResponse(USER_NOT_FOUND_MSSG % request.POST["userID"])
        if user == None:
            return HttpResponse(USER_NOT_FOUND_MSSG % request.session["userID"])
        if project == None:
            return HttpResponse(PROJECT_NOT_FOUND_MSSG % request.POST["projectID"])
        if user in project.members.all():
            project.members.add(newMember)
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
        if user  == None:
            return HttpResponse(USER_NOT_FOUND_MSSG % request.POST["userID"])
        if removedMember  == None:
            return HttpResponse(USER_NOT_FOUND_MSSG % request.POST["userID"])
        if project == None:
            return HttpResponse(PROJECT_NOT_FOUND_MSSG % request.POST["projectID"])
        if user == project.projectOwner:
            project.members.remove(removedMember)
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
# -- EDIT A TASK
# -- REMOVE A TASK
# -- MARK A TASK FOR VERIFICATION
# -- VERIIFY A TASK
# -- CHANGE TASK RESPONSIBLE
# -- REMOVE RESPONSIBLE FROM TASK
