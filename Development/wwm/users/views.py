from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from google.oauth2 import id_token
from google.auth.transport import requests
from .models import User

# Create your views here.
def index(request):
    try:
        if request.session['userID'] == None:
            redirect('/login')
        template = loader.get_template('users/index.html')
        contextUser = User.objects.get(id=request.session['userID'])
        context = {
                'user': contextUser,
                'tasks': contextUser.task_set.all(),
                'projects': contextUser.project_set.all()
        }
        return HttpResponse(template.render(context, request))
    except KeyError:
        return redirect('/login')


def login(request):
    template = loader.get_template('users/login.html')
    context = {}
    return HttpResponse(template.render(context, request))


def logout(request):
    request.session.pop('userID', None)
    return redirect('/login')


# CHECK USER VIEW
def verifyIdToken(token):
    try:
        idInfo = id_token.verify_oauth2_token(token, requests.Request(), "878193192072-cgl83u25orrhurjapo162hm3npg9801k.apps.googleusercontent.com")
        if idInfo['iss'] not in ['accounts.google.com', 'https://accounts.google.com']:
            raise ValueError("Wrong Issuer")
    except ValueError:
        return redirect('')


def userExistence(userEmail):
    try:
        existingUser = User.objects.get(email=userEmail) 
        return existingUser
    except:
        return False


def createNewUser(userInfo):
    newUser = User()
    newUser.firstName = userInfo["firstName"]
    newUser.lastName = userInfo["lastName"]
    newUser.email = userInfo["email"]
    newUser.rating = 5
    newUser.level = 0
    newUser.role = None
    newUser.save()
    return newUser


@csrf_exempt
def checkUser(request):
    if request.method == 'POST':
        requestIDToken = request.POST['idToken']
        verifyIdToken(requestIDToken)
        user = userExistence(request.POST['email'])
        mssg = "User retrieved"
        if user == False:
            user = createNewUser(request.POST) 
            mssg = "Create new user"
        request.session["userID"] = user.id
        return HttpResponse(mssg)
