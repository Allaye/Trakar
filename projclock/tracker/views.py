from django.db.models import F
from django.db.models.functions import Coalesce, Now
from rest_framework.generics import (CreateAPIView, DestroyAPIView, ListAPIView, UpdateAPIView)
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from tracker.serializers import (ProjectSerializer, ProjectActivitySerializer)
from tracker.models import Project, ProjectActivity
from employee.permissions import IsOwner, IsProjectMember, IsCurrentUser, IsProjectActive
from utils.analytics import get_total_project_activity_time, get_individual_project_activity_time

########################### Project ###########################

class CreateProjectApiview(CreateAPIView):
    """
    Create a new project object, and return the created object.
    permission_classes = "IsAuthenticated" :user is logged in , "IsAdminUser" : user is admin
    Post: /api/create/project
            
    """
    serializer_class = ProjectSerializer
    permission_classes = (IsAuthenticated, IsAdminUser) # protect the endpoint


    def perform_create(self, serializer):
        return serializer.save()


class RetriveMyProjectsApiView(ListAPIView):
    """
    Retrive all projects that the logged in user is a member of.
    permission_classes = "IsAuthenticated" :user is logged in 
    
    """
    serializer_class = ProjectSerializer
    permission_classes = (IsAuthenticated,) # protect the endpoint

    
    def get_queryset(self):
        return Project.objects.filter(members=self.request.user)

class RetriveProjectsApiView(ListAPIView):
    """
    Retrive all projects.
    permission_classes = "IsAuthenticated" :user is logged in, "IsAdminUser" : user is admin
    
    """
    serializer_class = ProjectSerializer
    permission_classes = (IsAuthenticated, IsAdminUser) # protect the endpoint

    
    def get_queryset(self):
        return Project.objects.all()
    
class RetriveOneProjectApiview(ListAPIView):
    """
    Retrive one project.
    permission_classes = "IsAuthenticated" :user is logged in, "IsAdminUser" : user is admin
    """
    serializer_class = ProjectSerializer
    permission_classes = (IsAuthenticated, ) # protect the endpoint

    
    def get_queryset(self):
        return Project.objects.filter(id=self.kwargs['id'])


class UpdateProjectApiview(UpdateAPIView):
    """
    Update a project object, and return the updated object.
    permission_classes = "IsAuthenticated" :user is logged in, "IsAdminUser" : user is admin
    """
    serializer_class = ProjectSerializer
    permission_classes = (IsAuthenticated, IsAdminUser) # protect the endpoint
    fields = ['title', 'description', 'technology', 'members', 'end_date']
    def perform_update(self, serializer):
        return serializer.save()

class DeleteProjectApiview(DestroyAPIView):
    """
    Delete a project object.
    Permission_classes = "IsAuthenticated" :user is logged in, "IsAdminUser" : user is admin
    """
    serializer_class = ProjectSerializer
    permission_classes = (IsAuthenticated, IsAdminUser) # protect the endpoint
    queryset = Project.objects.all()
    def perform_destroy(self, instance):
        instance.delete()


################## ProjectActivity ##############################

class CreateProjectActivityApiview(CreateAPIView):
    """
    Create a new project activity object, and return the created object.
    permission_classes = "IsAuthenticated" :user is logged in, "IsProjectMember" : user is a member of the project, "IsProjectActive" : project is active
    "IsCurrentUser" : user creating the object is current user
    """
    serializer_class = ProjectActivitySerializer
    permission_classes = (IsAuthenticated, IsProjectMember, IsCurrentUser, IsProjectActive) # protect the endpoint
    
    

    def perform_create(self, serializer):
        data = self.request.data
        project = Project.objects.filter(id=data['project']).prefetch_related('members')
        self.check_object_permissions(self.request, project)
        return serializer.save()

class RetriveProjectsActivitiesApiView(ListAPIView):
    """
    Retrive all project activities by current user
    permission_classes = "IsAuthenticated" :user is logged in
    """
    serializer_class = ProjectActivitySerializer
    permission_classes = (IsAuthenticated,) # protect the endpoint


    def get_queryset(self):
        return ProjectActivity.objects.filter(user=self.request.user)

class UpdateProjectActivityApiview(UpdateAPIView):
    """
    Update a project activity object, and return the updated object.
    permission_classes = "IsAuthenticated" :user is logged in, "IsOwner" : user is the owner of the project activity 
    """
    serializer_class = ProjectActivitySerializer
    permission_classes = (IsAuthenticated, IsOwner) # protect the endpoint
    fields = ['description', 'end_time']
    def perform_update(self, serializer):
        return serializer.save()

class DestroyProjectActivityApiview(DestroyAPIView):
    """
    Delete a project activity object.
    Permission_classes = "IsAuthenticated" :user is logged in, "IsOwner" : user is the owner of the project activity
    """
    serializer_class = ProjectActivitySerializer
    permission_classes = (IsAuthenticated, IsOwner)  # protect the endpoint
    queryset = ProjectActivity.objects.all()

    def perform_destroy(self, instance):
        return instance.delete()

class GetIndividualProjectActivityTime(APIView):
    """
    Retrive the total time spent on a project by a user.
    permission_classes = "IsAuthenticated" :user is logged in, "IsOwner" : user is the owner of the project activity or "IsAdminUser" : user is admin
    
    """
    serializer_class = ProjectActivitySerializer
    permission_classes = (IsAuthenticated, IsOwner|IsAdminUser) # protect the endpoint

    def get(self, request, *args, **kwargs):
        activities = ProjectActivity.objects.filter(user=self.kwargs['user'], project_id=self.kwargs['project']).annotate(end_or_now=Coalesce('end_time', Now())).annotate(duration=F('end_or_now')-F('start_time'))
        serializer = ProjectActivitySerializer(activities, many=True)
        return Response(get_individual_project_activity_time(serializer.data))

class GetTotalProjectActivityTime(APIView):
    """
    Retrive the total time spent on a project by all users.
    permission_classes = "IsAuthenticated" :user is logged in, "IsAdminUser" : user is admin
    
    """
    serializer_class = ProjectActivitySerializer
    permission_classes = (IsAuthenticated, IsOwner|IsAdminUser) # protect the endpoint

    def get(self, request, *args, **kwargs):
        activities = ProjectActivity.objects.filter(project_id=self.kwargs['project']).annotate(end_or_now=Coalesce('end_time', Now())).annotate(duration=F('end_or_now')-F('start_time'))
        serializer = ProjectActivitySerializer(activities, many=True)
        return Response(get_total_project_activity_time(serializer.data))