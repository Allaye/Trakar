from django.urls import path
from . import views


urlpatterns = [
    path('create/project', views.CreateProjectApiview.as_view(), name='add_project'),
    path('projects', views.RetriveProjectsApiView.as_view(), name='list_projects'),
    path('project/<int:pk>', views.RetrieveUpdateDeleteProjectApiview.as_view(), name='list_update_delete_project'),
]