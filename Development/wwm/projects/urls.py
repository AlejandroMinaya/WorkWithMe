from django.urls import path
from . import views

urlpatterns = [
            # PROJECTS
            path('', views.index),
            path('add', views.add),
            path('edit', views.edit),
            path('leave', views.leave),
            path('delete', views.delete),
            path('addMember', views.addMember),
            path('removeMember', views.removeMember),
        ]
