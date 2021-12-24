from rest_framework import permissions
from employee.models import Employee
from tracker.models import Project, ProjectActivity



class IsOwner(permissions.BasePermission):
    """
    Custom permission to only allow owners of an activity object to edit or delete it.
    """
    message = 'You are not the owner of this activity, so yoi can not edit or delete something you did not create.'

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permission to only allow 
        return obj.user == request.user

class IsProjectMember(permissions.BasePermission):
    """
    Custom permission to only allow members of a project to create an activity for it.
    """
    message = 'You are not a member or part of the team working on this project, so you cant create an activity for it.'
    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permissions are only allowed to the owner of the snippet.
        data = request.data
        project = Project.objects.filter(id=data['project']).prefetch_related('members')
        members = []
        for member in project:
            member_list = member.members.all()[:]
            for member in member_list:
                members.append(member.id)
        return request.user.id in  members

class IsCurrentUser(permissions.BasePermission):
    """
    Custom permission to only allow the current user to perform an action.
    """
    message = 'The user id provided is not the same as the current user, you cant create an activity for someone else.'

    def has_object_permission(self, request, view, obj):
        # Read permissions are allowed to any request,
        # so we'll always allow GET, HEAD or OPTIONS requests.
        if request.method in permissions.SAFE_METHODS:
            return True

        # Write permission to only allow current user create activity for themselves.
        id = request.data.get('user', None)
        return request.user.id == id