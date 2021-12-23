from rest_framework import permissions
from employee.models import Employee
from tracker.models import Project, ProjectActivity



class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an object to edit it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        return obj.user == request.user

class IsProjectMember(permissions.BasePermission):
    """
    Custom permission to only allow members of a project to create an activity for it.
    """

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        request_body = request.Post
        project_id = request_body['project']
        project = Project.objects.get(id=project_id)
        return request.user in  project.members