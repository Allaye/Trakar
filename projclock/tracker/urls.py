from django.urls import path
from . import views


urlpatterns = [
    path('create/project', views.CreateProjectApiview.as_view(), name='add_project'),
    path('projects', views.RetriveProjectsApiView.as_view(), name='list_projects'),
    path('projects/me', views.RetriveMyProjectsApiView.as_view(), name='list_my_projects'),
    path('project/<int:pk>', views.RetrieveUpdateDeleteProjectApiview.as_view(), name='list_update_delete_project'),
    path('create/activity', views.CreateProjectActivityApiview.as_view(), name='add_activity'),
    path('activitys', views.RetriveProjectsActivitiesApiView.as_view(), name='list_activities'),
    path('activity/<int:pk>', views.DestroyProjectActivityApiview.as_view(), name='list_update_delete_activity'),
]