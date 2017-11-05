from django.contrib.auth.models import User
from rest_framework import serializers
from courseroad.models import Subject


class SubjectSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)

    class Meta:
        model = Subject
        fields = 'semester', 'title', 'number', 'has_conflict', 'user'

class UserSerializer(serializers.ModelSerializer):
    subjects = serializers.PrimaryKeyRelatedField(many=True, queryset=Subject.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'subjects')


