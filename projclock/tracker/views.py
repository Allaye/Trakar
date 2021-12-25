from django.db.models import fields, Sum, F
from django.db.models.functions import Coalesce, Now
from django.http import request, response
from django.utils.dateparse import parse_duration
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import (CreateAPIView, DestroyAPIView, ListAPIView, UpdateAPIView, GenericAPIView)
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.response import Response
from tracker.serializers import (ProjectSerializer, ProjectActivitySerializer)
from tracker.models import Project, ProjectActivity
from employee.permissions import IsOwner, IsProjectMember, IsCurrentUser
from utils.analytics import get_total_project_activity_time, get_individual_project_activity_time

########################### Project ###########################

class CreateProjectApiview(CreateAPIView):
    """
    pytho
    
    """
    serializer_class = ProjectSerializer
    permission_classes = (IsAuthenticated, IsAdminUser) # protect the endpoint


    def perform_create(self, serializer):
        return serializer.save()


class RetriveMyProjectsApiView(ListAPIView):
    """
    
    
    """
    serializer_class = ProjectSerializer
    permission_classes = (IsAuthenticated,) # protect the endpoint

    
    def get_queryset(self):
        return Project.objects.filter(members=self.request.user)

class RetriveProjectsApiView(ListAPIView):
    """
    
    
    """
    serializer_class = ProjectSerializer
    permission_classes = (IsAuthenticated,) # protect the endpoint

    
    def get_queryset(self):
        return Project.objects.all()
    
class RetriveOneProjectApiview(ListAPIView):
    """
    
    
    """
    serializer_class = ProjectSerializer
    permission_classes = (IsAuthenticated,) # protect the endpoint

    
    def get_queryset(self):
        return Project.objects.filter(id=self.kwargs['id'])


class UpdateProjectApiview(UpdateAPIView):
    """
    
    
    """
    serializer_class = ProjectSerializer
    permission_classes = (IsAuthenticated, IsAdminUser) # protect the endpoint
    fields = ['title', 'description', 'technology', 'members', 'end_date']
    def perform_update(self, serializer):
        return serializer.save()

class DeleteProjectApiview(DestroyAPIView):
    """
    
    
    """
    serializer_class = ProjectSerializer
    permission_classes = (IsAuthenticated, IsAdminUser) # protect the endpoint
    queryset = Project.objects.all()
    def perform_destroy(self, instance):
        instance.delete()


################## ProjectActivity ##############################

class CreateProjectActivityApiview(CreateAPIView):
    """
    
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
    
    """
    serializer_class = ProjectActivitySerializer
    permission_classes = (IsAuthenticated,) # protect the endpoint


    def get_queryset(self):
        return ProjectActivity.objects.filter(user=self.request.user)

class UpdateProjectActivityApiview(UpdateAPIView):
    """
    
    """
    serializer_class = ProjectActivitySerializer
    permission_classes = (IsAuthenticated, IsOwner) # protect the endpoint
    fields = ['description', 'end_time']
    def perform_update(self, serializer):
        return serializer.save()

class DestroyProjectActivityApiview(DestroyAPIView):
    """
    
    """
    serializer_class = ProjectActivitySerializer
    permission_classes = (IsAuthenticated, IsOwner)  # protect the endpoint


    def perform_destroy(self, instance):
        return instance.delete()

class GetIndividualProjectActivityTime(APIView):
    """
    
    """
    serializer_class = ProjectActivitySerializer
    permission_classes = (IsAuthenticated, IsOwner|IsAdminUser) # protect the endpoint

    def get(self, request, *args, **kwargs):
        activities = ProjectActivity.objects.filter(user=self.kwargs['user'], project_id=self.kwargs['project']).annotate(end_or_now=Coalesce('end_time', Now())).annotate(duration=F('end_or_now')-F('start_time'))
        serializer = ProjectActivitySerializer(activities, many=True)
        return Response(get_individual_project_activity_time(serializer.data))

class GetTotalProjectActivityTime(APIView):
    """
    
    """
    serializer_class = ProjectActivitySerializer
    permission_classes = (IsAuthenticated, IsOwner|IsAdminUser) # protect the endpoint

    def get(self, request, *args, **kwargs):
        activities = ProjectActivity.objects.filter(project_id=self.kwargs['project']).annotate(end_or_now=Coalesce('end_time', Now())).annotate(duration=F('end_or_now')-F('start_time'))
        serializer = ProjectActivitySerializer(activities, many=True)
        return Response(get_total_project_activity_time(serializer.data))