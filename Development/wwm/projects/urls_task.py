from django.urls import path
from . import views

urlpatterns = [
            # TASKS
            path('add', views.addTask),
            path('remove', views.removeTask),
            path('markTaskForVerification', views.markTaskForVerification),
            path('verify', views.verifyTask),
            path('changeResponsible', views.changeTaskResponsible),
        ]
