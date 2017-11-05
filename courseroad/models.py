from django.db import models

# Create your models here.

class Subject(models.Model):
    semester = models.IntegerField(default=0)
    number = models.CharField(max_length=10)
    title = models.CharField(max_length=200, blank=False)
    has_conflict = models.BooleanField(default=False)
    user = models.ForeignKey('auth.User', related_name='subjects', on_delete=models.CASCADE)

    class Meta:
        ordering = ('number',)


# class CoreSubject(models.Model):
#     termCode = models.CharField(max_length=7)
#     subjectId = models.CharField(max_length=10)
#     academicYear = models.IntegerField(max_length=4)
#     title = models.CharField(max_length=200, blank=False)
#     cluster = models.CharField()
#     prerequisites = models.TextField()
#     units = models.TextField()
#     optional = models.TextField(default='')
#     description = models.TextField()
#     instructors = models.TextField()
