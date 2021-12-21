from django.urls import path
from django.urls.resolvers import URLPattern
from . import views


urlpatterns = [
    path('create/project', views.CreateProjectApiview.as_view(), name='projects'),
    path('projects', views.RetriveProjectsApiView.as_view(), name='projects'),
    path('update/project/<int:pk>', views.UpdateProjectApiview.as_view(), name='projects'),
]