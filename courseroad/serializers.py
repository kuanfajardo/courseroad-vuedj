from django.contrib.auth.models import User
from rest_framework import serializers
from courseroad.models import Subject, UserSubject, Semester, Year, Bucket
from rest_framework import validators


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = "__all__"


class UserSubjectSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)
    semester = serializers.IntegerField(source='semester.semester_id', read_only=True)
    subject = SubjectSerializer(many=False, read_only=True)

    class Meta:
        model = UserSubject
        fields = ('semester', 'has_conflict', 'user', 'subject')


class SemesterSerializer(serializers.ModelSerializer):
    subjects = UserSubjectSerializer(many=True, read_only=True)
    year = serializers.IntegerField(source='year.year_id', read_only=True)

    class Meta:
        model = Semester
        fields = "hidden", "type", "year", "semester_id", "subjects"


class YearSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)
    semesters = SemesterSerializer(many=True, read_only=True)

    class Meta:
        model = Year
        fields =  "user", "semesters", "title", "year_id"


class BucketSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)
    json = serializers.JSONField(default={})

    class Meta:
        model = Bucket
        exclude = ('requirement_obj', 'user')


class UserSerializer(serializers.ModelSerializer):
    subjects = UserSubjectSerializer(many=True)
    years = YearSerializer(many=True, read_only=True)
    buckets = BucketSerializer(many=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'subjects', "years", "buckets")
