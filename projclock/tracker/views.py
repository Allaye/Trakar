from functools import partial
from rest_framework import serializers
from rest_framework.generics import (CreateAPIView, ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView, UpdateAPIView)
from tracker.serializers import (ProjectSerializer, ProjectActivitySerializer)
from tracker.models import Project, ProjectActivity
# Create your views here.

class CreateProjectApiview(CreateAPIView):
    """
    
    
    """
    serializer_class = ProjectSerializer

    def perform_create(self, serializer):
        return serializer.save()


class RetriveProjectsApiView(ListAPIView):
    """
    
    
    """
    serializer_class = ProjectSerializer
    
    def get_queryset(self):
        return Project.objects.all()
    

class UpdateProjectApiview(RetrieveUpdateDestroyAPIView):
    """
    
    """
    serializer_class = ProjectSerializer

    def get_queryset(self):
        return Project.objects.all()

    # def update(self, request, *args, **kwargs):
    #     partial = kwargs.pop('partial', False)
    #     instance = self.get_object()
    #     serializer = self.get_serializer(instance, data=request.data, partial=partial)
    #     serializer.is_valid(raise_exception=True)
    #     self.perform_update(serializer)
    #     return Response(serializer.data)
    #     return super().update(request, *args, **kwargs)


class CreateProjectActivityApiview(CreateAPIView):
    """
    
    """
    serializer_class = ProjectActivitySerializer

    def perform_create(self, serializer):
        return serializer.save()

class RetriveProjectsActivitiesApiView(ListAPIView):
    """
    
    """
    serializer_class = ProjectActivitySerializer

    def get_queryset(self):
        return ProjectActivity.objects.all()

class UpdateProjectActivityApiview(RetrieveUpdateDestroyAPIView):
    """
    
    """
    serializer_class = ProjectActivitySerializer

    def get_queryset(self):
        return ProjectActivity.objects.all()