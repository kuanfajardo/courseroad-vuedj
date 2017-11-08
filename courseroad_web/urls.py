"""courseroad_web URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""

from django.conf.urls import url, include
from rest_framework import routers
from courseroad import views

# router = routers.DefaultRouter()
# router.register(r'users', views.UserViewSet)
# router.register(r'groups', views.GroupViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    # url(r'^', include(router.urls)),
    url(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    url(r'^subjects/$', views.SubjectList.as_view()),
    url(r'^subjects/(?P<pk>[A-Za-z0-9.]+)/$', views.SubjectDetail.as_view()),
    url(r'^users/$', views.UserList.as_view()),
    # url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),
    url(r'^user_subjects/$', views.UserSubjectList.as_view()),
    url(r'^user_subjects/(?P<pk>[A-Za-z0-9.]+)/$', views.UserSubjectDetail.as_view()),
    # url(r'^years/$', views.YearList.as_view()),
    # url(r'^years/(?P<pk>[A-Za-z0-9.]+)/$', views.YearDetail.as_view()),
    url(r'^semesters/$', views.SemesterList.as_view()),
    url(r'^semesters/(?P<pk>[A-Za-z0-9.]+)/$', views.SemesterDetail.as_view()),

    url(r'^users/(?P<username>[A-Za-z0-9]+)/$', views.UserDetail.as_view()),
    url(r'^users/(?P<username>[A-Za-z0-9]+)/years/$', views.YearList.as_view()),
    url(r'^users/(?P<username>[A-Za-z0-9]+)/years/(?P<year_id>[0-9]+)/$', views.YearDetail.as_view()),
    url(r'^users/(?P<username>[A-Za-z0-9]+)/years/(?P<year_id>[0-9]+)/semesters/$', views.SemesterList.as_view()),
    url(r'^users/(?P<username>[A-Za-z0-9]+)/years/(?P<year_id>[0-9]+)/semesters/(?P<semester_id>[0-9]+)/$', views.SemesterDetailLong.as_view()),
    url(r'^users/(?P<username>[A-Za-z0-9]+)/years/(?P<year_id>[0-9]+)/semesters/(?P<semester_id>[0-9]+)/subjects/$', views.UserSubjectList.as_view()),
    url(r'^users/(?P<username>[A-Za-z0-9]+)/years/(?P<year_id>[0-9]+)/semesters/(?P<semester_id>[0-9]+)/subjects/(?P<pk>[A-Za-z0-9.]+)/$', views.UserSubjectDetail.as_view()),
]
