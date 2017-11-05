from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import viewsets
from courseroad.serializers import UserSerializer, SubjectSerializer
from courseroad.models import Subject
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework import generics



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


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

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

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

class SubjectDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = Subject.objects.all()
    serializer_class = SubjectSerializer


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
