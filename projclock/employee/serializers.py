from rest_framework import serializers
from employee.models import Employee


class RegisterApiViewSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=125, min_length=5, write_only=True)


    class Meta:
        model = Employee
        fields = ('id', 'username', 'email', 'password', 'is_staff')

    def create(self, validated_data):
        return Employee.objects.create_user(**validated_data)

class LoginApiViewSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)


    class Meta:
        model = Employee
        fields = ('email', 'password', 'token', 'is_staff')

        read_only_fields = ['token']