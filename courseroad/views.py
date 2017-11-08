from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import viewsets
from courseroad.serializers import UserSerializer, SubjectSerializer, UserSubjectSerializer, YearSerializer, SemesterSerializer
from courseroad.models import Subject, UserSubject, Year, Semester
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics
from rest_framework import permissions
from django.core.exceptions import MultipleObjectsReturned

from courseroad.permissions import IsOwnerOrReadOnly
from courseroad.engine import Road

from courseroad.engine import run

# class UserViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows users to be viewed or edited.
#     """
#     queryset = User.objects.all().order_by('-date_joined')
#     serializer_class = UserSerializer


# class UserList(APIView):
#     """
#     List all users, or create user
#     """
#     def get(self, request, format=None):
#         users = User.objects.all()
#         serializer = UserSerializer(users, many=True)
#         return Response(serializer.data)
#
#     def post(self, request, format=None):
#         serializer = UserSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAdminUser,)

class UserDetail(generics.RetrieveAPIView):
    lookup_field = 'username'
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAdminUser,)

class UserSubjectList(generics.ListCreateAPIView):
    queryset = UserSubject.objects.all()
    serializer_class = UserSubjectSerializer
    # permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        year = str(self.request.stream.path).split('/')[4]
        semester = str(self.request.stream.path).split('/')[6]

        year_obj = Year.objects.get(year_id=year, user=self.request.user)
        semester_obj = Semester.objects.get(semester_id=semester, year=year_obj)

        serializer.save(semester=semester_obj, user=self.request.user)

class UserSubjectDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = UserSubject.objects.all()
    serializer_class = UserSubjectSerializer
    permission_classes = (IsOwnerOrReadOnly,)

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

class SemesterList(generics.ListCreateAPIView):
    queryset = Semester.objects.all()
    serializer_class = SemesterSerializer

    def perform_create(self, serializer):
        year = str(self.request.stream.path).split('/')[-3]
        serializer.save(year=Year.objects.filter(year_id=year)[0])

class SemesterDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Semester.objects.all()
    serializer_class = SemesterSerializer
    lookup_field = 'semester_id'
    lookup_url_kwarg = 'pk'


    def get_queryset(self):
        # print(str(self.))
        user = self.request.user
        return Semester.objects.all()

    # def get(self, request, *args, **kwargs):
    #     print(kwargs['year_id'])


class SemesterDetailLong(APIView):
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
        return Response


# class UserDetail(APIView):
#     """
#     Retrieve, update or delete a user instance.
#     """
#     def get_object(self, pk):
#         try:
#             return User.objects.get(pk=pk)
#         except User.DoesNotExist:
#             raise Http404
#
#     def get(self, request, pk, format=None):
#         user = self.get_object(pk)
#         serializer = UserSerializer(user, many=True)
#         return Response(serializer.data)
#
#     def put(self, request, pk, format=None):
#         user = self.get_object(pk)
#         serializer = UserSerializer(user, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, pk, format=None):
#         user = self.get_object(pk)
#         user.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
#


class SubjectList(generics.ListCreateAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = (permissions.IsAdminUser,)

    # def perform_create(self, serializer):
    #     print(self.request.data["prerequisites"])

class SubjectDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer
    permission_classes = (permissions.IsAdminUser,)

    # def perform_update(self, serializer):
    #     serializer.save(prerequisites=list(self.request["prerequisites"]))


# class SubjectList(APIView):
#     """
#     List all subjects, or create subject
#     """
#     def get(self, request, format=None):
#         subjects = Subject.objects.all()
#         serializer = SubjectSerializer(subjects, many=True)
#         return Response(serializer.data)
#
#     def post(self, request, format=None):
#         serializer = SubjectSerializer(data=request.data)
#         print("123456756454343556453423")
#         if serializer.is_valid():
#             print("--------d-d-d-d-d-d-d-")
#             serializer.save()
#             print("--------f-f-f-f-f-f-f-")
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def perform_create(self, serializer):
#         serializer.save(user=self.request.user)
#
#
# class SubjectDetail(APIView):
#     """
#     Retrieve, update or delete a subject instance.
#     """
#     def get_object(self, pk):
#         try:
#             return Subject.objects.get(pk=pk)
#         except User.DoesNotExist:
#             raise Http404
#
#     def get(self, request, pk, format=None):
#         subject = self.get_object(pk)
#         serializer = SubjectSerializer(subject)
#         return Response(serializer.data)
#
#     def put(self, request, pk, format=None):
#         subject = self.get_object(pk)
#         serializer = SubjectSerializer(subject, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#
#     def delete(self, request, pk, format=None):
#         subject = self.get_object(pk)
#         subject.delete()
#         return Response(status=status.HTTP_204_NO_CONTENT)
#




# class GroupViewSet(viewsets.ModelViewSet):
#     """
#     API endpoint that allows groups to be viewed or edited.
#     """
#     queryset = Group.objects.all()
#     serializer_class = GroupSerializer


class Rules(APIView):

    def get_subjects(self, user):
        subjects = {}

        for year in Year.objects.filter(user=user):
            temp = {}

            for semester in Semester.objects.filter(year=year):
                subj = []

                for subject in UserSubject.objects.filter(semester=semester):
                    subj.append(subject.number)

                temp[semester.semester_id] = subj

            subjects[year.year_id] = temp

        return subjects

    def get(self, request, a, b, format=None):
        subjects = self.get_subjects(request.user)

        r = Road(subjects)
        sat_dict = r.check_pre_reqs()

        for subject in sat_dict:
            subject_obj = UserSubject.objects.get(user=request.user, number=subject)
            subject_obj.has_conflict = not sat_dict[subject]
            subject_obj.save()

        return Response(status=status.HTTP_204_NO_CONTENT)


        # req_file = open('courseroad/static/courseroad/6-3.req')
        # for s in subjects:
        #     print(s.number, s.semester.semester_id)
        # run(subjects, req_file)

