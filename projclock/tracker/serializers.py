from django.db.models import fields
from rest_framework import serializers
from tracker.models import Project, ProjectActivity, Employee


class ProjectSerializer(serializers.ModelSerializer):

    class Meta:
        model = Project
        fields = '__all__'
        extra_kwargs = {'title': {'required': False},'description': {'required': False},'technology': {'required': False},'members': {'required': False}}



class ProjectActivitySerializer(serializers.ModelSerializer):

    class Meta:
        model = ProjectActivity
        fields = '__all__'