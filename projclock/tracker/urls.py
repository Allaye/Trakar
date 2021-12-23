from django.urls import path
from . import views


urlpatterns = [
    ############## Project ##############
    path('create/project', views.CreateProjectApiview.as_view(), name='add_project'),
    path('projects', views.RetriveProjectsApiView.as_view(), name='list_projects'),
    path('projects/me', views.RetriveMyProjectsApiView.as_view(), name='list_my_projects'),
    path('project/<int:id>', views.RetriveOneProjectApiview.as_view(), name='list_a_project'),
    path('project/update/<int:id>', views.UpdateProjectApiview.as_view(), name='update_project'),
    path('project/delete/<int:pk>', views.DeleteProjectApiview.as_view(), name='delete_project'),
    ############# ProjectActivity #############
    path('create/activity', views.CreateProjectActivityApiview.as_view(), name='add_activity'),
    path('activitys', views.RetriveProjectsActivitiesApiView.as_view(), name='list_activities'),
    path('activity/update/<int:id>', views.UpdateProjectActivityApiview.as_view(), name='list_a_activity'),
    path('activity/delete/<int:id>', views.DestroyProjectActivityApiview.as_view(), name='list_update_delete_activity'),
]