from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework import validators

# Create your models here.


class Subject(models.Model):
    termCode = models.CharField(max_length=7)
    subjectId = models.CharField(max_length=10)
    academicYear = models.IntegerField()
    title = models.CharField(max_length=200, blank=False)
    cluster = models.TextField()
    prerequisites = models.TextField()
    units = models.TextField()
    optional = models.TextField(default='')
    description = models.TextField()
    instructors = models.TextField()

class UserSubject(models.Model):
    # semester = models.IntegerField(default=0)
    semester = models.ForeignKey('courseroad.Semester', related_name='subjects', on_delete=models.CASCADE)
    # number = models.CharField(max_length=10)
    # title = models.CharField(max_length=200, blank=False)
    has_conflict = models.BooleanField(default=False)
    user = models.ForeignKey('auth.User', related_name='subjects', on_delete=models.CASCADE)

    subject = models.ForeignKey('courseroad.Subject', default=None)


class Semester(models.Model):
    year = models.ForeignKey('courseroad.Year', related_name='semesters', on_delete=models.CASCADE)
    semester_id = models.IntegerField()
    hidden = models.BooleanField(default=False)
    # subjects = models.ForeignKey('courseroad.UserSubject', related_name='semester', on_delete=models.CASCADE)
    type = models.CharField(max_length=10)
    # user = models.ForeignKey('auth.User')

    class Meta:
        ordering = ('semester_id',)


class Year(models.Model):
    # semesters = models.ForeignKey('courseroad.Semester', related_name='year', on_delete=models.CASCADE)
    user = models.ForeignKey('auth.User', related_name='years', on_delete=models.CASCADE)
    title = models.CharField(max_length=20)
    year_id = models.IntegerField()

    class Meta:
        ordering = ('year_id',)





    class Meta:



