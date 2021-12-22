from rest_framework import serializers
from tracker.models import Project, ProjectActivity


class ProjectSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Project
        fields = '__all__'
        extra_kwargs = {'title': {'required': False},'description': {'required': False},'technology': {'required': False},'members': {'required': False}}



class ProjectActivitySerializer(serializers.ModelSerializer):
    is_running = serializers.ReadOnlyField()
    duration = serializers.ReadOnlyField()
    
    class Meta:
        model = ProjectActivity
        fields = '__all__'