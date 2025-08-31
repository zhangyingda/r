# RESTful API
from django.contrib.auth.models import Group
from rest_framework import serializers
from .models import Student, CustomUser

class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields= '__all__'


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'groups']


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ['url', 'name']