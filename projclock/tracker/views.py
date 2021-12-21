from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.generics import (CreateAPIView, DestroyAPIView, ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView)
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.filters import SearchFilter, OrderingFilter
from rest_framework.generics import (CreateAPIView, ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView, UpdateAPIView)
from tracker.serializers import (ProjectSerializer, ProjectActivitySerializer)
from tracker.models import Project, ProjectActivity
# Create your views here.

class CreateProjectApiview(CreateAPIView):
    """
    pytho
    
    """
    serializer_class = ProjectSerializer
    permission_classes = (IsAuthenticated, IsAdminUser) # protect the endpoint


    def perform_create(self, serializer):
        return serializer.save()


class RetriveProjectsApiView(ListAPIView):
    """
    
    
    """
    serializer_class = ProjectSerializer
    permission_classes = (IsAuthenticated, IsAdminUser) # protect the endpoint

    
    def get_queryset(self):
        return Project.objects.filter(owner=self.request.user)
    

class RetrieveUpdateDeleteProjectApiview(RetrieveUpdateDestroyAPIView):
    """
    
    """
    serializer_class = ProjectSerializer
    permission_classes = (IsAuthenticated, IsAdminUser) # protect the endpoint


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
    permission_classes = (IsAuthenticated,) # protect the endpoint


    def perform_create(self, serializer):
        return serializer.save()

class RetriveProjectsActivitiesApiView(ListAPIView):
    """
    
    """
    serializer_class = ProjectActivitySerializer
    permission_classes = (IsAuthenticated,) # protect the endpoint


    def get_queryset(self):
        return ProjectActivity.objects.filter(owner=self.request.user)

class DestroyProjectActivityApiview(DestroyAPIView):
    """
    
    """
    serializer_class = ProjectActivitySerializer
    permission_classes = (IsAuthenticated,) # protect the endpoint


    def get_queryset(self):
        return ProjectActivity.objects.all()