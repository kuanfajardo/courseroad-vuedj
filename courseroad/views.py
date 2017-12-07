from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import viewsets
from courseroad.serializers import UserSerializer, SubjectSerializer, UserSubjectSerializer, YearSerializer, SemesterSerializer, BucketSerializer
from courseroad.models import Subject, UserSubject, Year, Semester, Bucket
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework import permissions
from django.core.exceptions import ObjectDoesNotExist
from django.core.exceptions import MultipleObjectsReturned

from courseroad.permissions import IsOwnerOrReadOnly
from courseroad.engine import Road, RequirementFactory


class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAdminUser,)


class UserDetail(generics.RetrieveAPIView):
    lookup_field = 'username'
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAdminUser,)


class UserSubjectList(APIView):

    def get(self, request, username, year_id, semester_id):
        year = Year.objects.get(user=request.user, year_id=year_id)
        semester = Semester.objects.get(year=year, semester_id=semester_id)
        subjects = UserSubject.objects.filter(user=request.user, semester=semester)

        serializer = UserSubjectSerializer(subjects, many=True)
        return Response(serializer.data)

    def get_subject(self, subject_id):
        try:
            return Subject.objects.get(subjectId=subject_id)
        except ObjectDoesNotExist:
            return None

    def post(self, request, username, year_id, semester_id):
        year = Year.objects.get(user=request.user, year_id=year_id)
        semester = Semester.objects.get(year=year, semester_id=semester_id)
        subject = self.get_subject(request.data['subjectID'])

        if subject is None:
            return Response(status=status.HTTP_400_BAD_REQUEST, data={"error_type": 0})

        print(request)
        serializer = UserSubjectSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(subject=subject, user=request.user, semester=semester)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserSubjectDetail(APIView):
    """
    Retrieve, update or delete a user instance.
    """
    def get_object(self, year_id, semester_id, subject_id, user):
        try:
            print("yetet")

            print(user.username)
            year = Year.objects.get(user=user, year_id=year_id)
            print(year)
            semester = Semester.objects.get(year=year, semester_id=semester_id)
            print(semester)
            subject = Subject.objects.get(subjectId=subject_id)
            return UserSubject.objects.get(semester=semester, subject=subject)
        except:
            raise Http404

    def get(self, request, year_id, username, semester_id, subject_id, format=None):
        print(subject_id, year_id, username, semester_id)
        subject = self.get_object(year_id, semester_id, subject_id, request.user)
        serializer = UserSubjectSerializer(subject)
        return Response(serializer.data)

    def put(self, request, year_id, username, semester_id, subject_id, format=None):
        subject = self.get_object(year_id, semester_id, subject_id, request.user)
        serializer = UserSubjectSerializer(subject, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, year_id, username, semester_id, subject_id, format=None):
        print("dfg")
        subject = self.get_object(year_id, semester_id, subject_id, request.user)
        subject.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


    def options(self, request, *args, **kwargs):
        print(request)
        print("yeter")
        return Response(status=status.HTTP_200_OK)


class YearList(generics.ListCreateAPIView):
    queryset = Year.objects.all()
    serializer_class = YearSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class YearDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Year.objects.all()
    serializer_class = YearSerializer
    lookup_field = 'year_id'

    def get_queryset(self):
        user = self.request.user
        return Year.objects.filter(user=user)


class SemesterList(APIView):
    def get(self, request, username, year_id):
        year = Year.objects.get(user=request.user, year_id=year_id)
        semesters = Semester.objects.filter(year=year)
        serializer = SemesterSerializer(semesters, many=True)

        return Response(serializer.data)

    def post(self, request, username, year_id):
        year = Year.objects.get(user=request.user, year_id=year_id)

        serializer = SemesterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(year=year)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SemesterDetail(APIView):
    """
    Retrieve, update or delete a user instance.
    """
    def get_object(self, year_id, semester_id, user):
        try:
            year = Year.objects.get(user=user, year_id=year_id)
            return Semester.objects.get(year=year, semester_id=semester_id)
        except:
            raise Http404

    def get(self, request, year_id, username, semester_id, format=None):
        semester = self.get_object(year_id, semester_id, request.user)
        serializer = SemesterSerializer(semester)
        return Response(serializer.data)

    def put(self, request, year_id, username, semester_id, format=None):
        semester = self.get_object(year_id, semester_id, request.user)
        serializer = SemesterSerializer(semester, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, year_id, username, semester_id, format=None):
        semester = self.get_object(year_id, semester_id, request.user)
        semester.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class SubjectList(generics.ListCreateAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = (permissions.IsAdminUser,)


class SubjectDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = (permissions.IsAdminUser,)


class BucketList(APIView):
    def get(self, request, username):
        buckets = Bucket.objects.filter(user=request.user)
        serializer = BucketSerializer(buckets, many=True)

        return Response(serializer.data)

    def post(self, request, username):
        serializer = BucketSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BucketDetail(APIView):
    pass


class Rules(APIView):

    def get_road(self, user):
        road = {}

        for year in Year.objects.filter(user=user):
            temp = {}

            for semester in Semester.objects.filter(year=year):
                subj = []

                for subject in UserSubject.objects.filter(semester=semester):
                    subj.append(subject.subject.subjectId)

                temp[semester.semester_id] = subj

            road[year.year_id] = temp

        return road

    def get_reqs(self, user):
        reqs = {}
        #
        # for req in Bucket.object.filter(user=user):
        #     reqs[req.name] = req.requirements_obj

        return reqs

    def get(self, request, format=None):
        road_dict = self.get_road(request.user)
        req_dict = self.get_reqs(request.user)

        r = Road(road_dict, req_dict)

        # Check pre-requisites
        sat_dict = r.check_pre_reqs()

        for subject in sat_dict:
            subject_obj = Subject.objects.get(subjectId=subject)
            user_subject_obj = UserSubject.objects.get(user=request.user, subject=subject_obj)
            user_subject_obj.has_conflict = not sat_dict[subject]
            user_subject_obj.save()

        # Check course
        # bucket_dict = r.check_buckets()
        #
        # for bucket in bucket_dict:
        #     bucket_obj = Bucket.objects.get(user=request.user, name=bucket)
        #     bucket_obj.json = bucket_dict[bucket]

        return Response(status=status.HTTP_204_NO_CONTENT)



