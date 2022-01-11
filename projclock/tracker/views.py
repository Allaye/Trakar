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
    - Endpoint: Post: /api/create/project
    - Authorization: Bearer <eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImEiLCJlbWFpbCI6ImFAZW1haWwuY29tIiwiZXhwIjoxNjQxMDUyMjI0fQ.unXe-dxoFCEY5l2VGkeRR8ue-Ggr6YxQS2nJUA63VZ4>
    - Request body:{
    "name": "project pholoa",
    "description": "blockchain systems to track spent time",
    "technology": {"technology":"blockchain"},
    "members": [1,4,2]           // this are the members ids added to the project (project members)
    "start_date": "2022-01-01",  // if left blank it defaults to today
    }

    - Response:{
    "id": 3,
    "is_completed": false,
    "title": "",
    "description": "blockchain systems to track spent time",
    "technology": {
        "technology": "blockchain"
    },
    "start_date": "2022-01-01",
    "end_date": null,
    "members": [
        1, 4, 2
    ]
    }

    """
    serializer_class = ProjectSerializer
    permission_classes = (IsAuthenticated, IsAdminUser) # protect the endpoint


    def perform_create(self, serializer):
        return serializer.save()


class RetriveMyProjectsApiView(ListAPIView):
    """
    Retrive all projects that the logged in user is a member of.
    permission_classes = "IsAuthenticated" :user is logged in
    Get: /api/projects
    response:
    {
         "id": 3,
    "is_completed": false,
    "title": "",
    "description": "blockchain systems to track spent time",
    "technology": {
        "technology": "blockchain"
    },
    "start_date": "2022-01-01",
    "end_date": null,
    "members": [
        1, 4, 2
    ]
    }
    
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
    Endpoint PATCH api/project/update/1/
      Authorization: Bearer <eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImEiLCJlbWFpbCI6ImFAZW1haWwuY29tIiwiZXhwIjoxNjQxMDUyMjI0fQ.unXe-dxoFCEY5l2VGkeRR8ue-Ggr6YxQS2nJUA63VZ4>
      Request body:{
        "start_date": "2022-01-01",
        "end_date": 2022-10-10,
        }
      Response{
        "id": 1,
        "is_completed": true,
        "title": "title here",
        "description": "blockchain systems to track spent time",
        "technology": {
            "technology": "blockchain"
        },
        "start_date": "2022-01-01",
        "end_date": "2022-10-10",
        "members": [
            1, 4, 2
        ]
        }

    """
    serializer_class = ProjectSerializer
    permission_classes = (IsAuthenticated, IsAdminUser) # protect the endpoint
    queryset = Project.objects.all()
    fields = ['title', 'description', 'technology', 'members', 'end_date']
    def perform_update(self, serializer):
        return serializer.save()

class DeleteProjectApiview(DestroyAPIView):
    """
    Delete a project object.
    Permission_classes = "IsAuthenticated" :user is logged in, "IsAdminUser" : user is admin
        Endpoint DELETE api/project/delete/1/
        Authorization: Bearer <eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ1c2VybmFtZSI6ImEiLCJlbWFpbCI6ImFAZW1haWwuY29tIiwiZXhwIjoxNjQxMDUyMjI0fQ.unXe-dxoFCEY5l2VGkeRR8ue-Ggr6YxQS2nJUA63VZ4>

        Response{
        "message": "Project deleted successfully"
        }
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
    Endpoint POST api/project/activity/create/1/
    """
    serializer_class = ProjectActivitySerializer
    permission_classes = (IsAuthenticated, IsProjectMember, IsCurrentUser) # protect the endpoint
    


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
    queryset = ProjectActivity.objects.all()
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
    Response{
        "total_time": "8 days, 11:08:10",
        "user": 1
        }
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
    
    Response{
        "total_time": "30 days, 11:08:10",
        "project": 1
        }
    """
    serializer_class = ProjectActivitySerializer
    permission_classes = (IsAuthenticated, IsOwner|IsAdminUser) # protect the endpoint

    def get(self, request, *args, **kwargs):
        activities = ProjectActivity.objects.filter(project_id=self.kwargs['project']).annotate(end_or_now=Coalesce('end_time', Now())).annotate(duration=F('end_or_now')-F('start_time'))
        serializer = ProjectActivitySerializer(activities, many=True)
        
        return Response(get_total_project_activity_time(serializer.data))