from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from gaskserv import views

urlpatterns = [
    url(r'^gasks/$', views.GaskList.as_view()),
    url(r'^gasks/(?P<pk>[0-9]+)/$', views.GaskDetail.as_view()),

    url(r'^timed/$', views.TimeEntryList.as_view()),
    url(r'^timed/(?P<pk>[0-9]+)/$', views.TimeEntryDetail.as_view()),

    url(r'^users/$', views.UserList.as_view()),
    url(r'^users/(?P<pk>[0-9]+)/$', views.UserDetail.as_view()),

    url(r'^posts/$', views.PostList.as_view()),
    url(r'^posts/(?P<pk>[0-9]+)/$', views.PostDetail.as_view()),

    url(r'^projects/$', views.ProjectList.as_view()),
    url(r'^projects/(?P<pk>[0-9]+)/$', views.ProjectDetail.as_view()),

    url(r'^teams/$', views.TeamList.as_view()),
    url(r'^teams/(?P<pk>[0-9]+)/$', views.TeamDetail.as_view()),

    url(r'^issues/$', views.IssueList.as_view()),
    url(r'^issues/(?P<pk>[0-9]+)/$', views.IssueDetail.as_view()),

    url(r'^threads/$', views.ThreadList.as_view()),
    url(r'^threads/(?P<pk>[0-9]+)/$', views.ThreadDetail.as_view()),

    url(r'^login/$', views.LoginView.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
