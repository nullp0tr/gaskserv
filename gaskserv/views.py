from rest_framework import generics, permissions
from gaskserv.permissions import *
from gaskserv.models import *
from gaskserv.serializers import *
from django.utils import timezone



###############################
######## TIME ENTRIAS #########

class TimeEntryDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly)
    queryset = TimeEntry.objects.all()
    serializer_class = TimeEntrySerializer

    def perform_update(self, serializer):
        serializer.save(end_time=timezone.now())


class TimeEntryList(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly, HasAllEntriesValid)
    serializer_class = TimeEntrySerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        queryset = TimeEntry.objects.filter(owner=self.request.user)
        last_entry = self.request.query_params.get('last_entry', None)
        if last_entry is not None and last_entry == 'true':
            queryset = queryset.filter(end_time=None)
        return queryset

#########################
######## GASKAS ########


class GaskDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (IsAuthenticated, IsOwnerOrReadOnly,)
    queryset = Gask.objects.all()
    serializer_class = GaskSerializer


class GaskList(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated, IsOwnerOrReadOnly,)
    queryset = Gask.objects.exclude(object_id__isnull=False)
    serializer_class = GaskSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


#########################
######## USERAS #########

class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


########################
####### POSTAS #########

class PostDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostList(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)
    queryset = Post.objects.all()
    serializer_class = PostSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


##########################
####### PROJECTS #########

class ProjectDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsMemberOrOwnerOrReadOnly,)
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class ProjectList(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


##########################
######## TEAMS ###########

class TeamDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
    queryset = Team.objects.all()
    serializer_class = TeamSerializer


class TeamList(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)
    queryset = Team.objects.all()
    serializer_class = TeamSerializer


##########################
######## ISSUES ##########

class IssueDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)
    queryset = Issue.objects.all()
    serializer_class = IssueSerializer


class IssueList(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)
    queryset = Issue.objects.exclude(object_id__isnull=False)
    serializer_class = IssueSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


##########################
######## THREADS #########

class ThreadDetail(generics.RetrieveUpdateDestroyAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)
    queryset = Thread.objects.all()
    serializer_class = ThreadSerializer


class ThreadList(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly,)
    queryset = Thread.objects.exclude(object_id__isnull=False)
    serializer_class = ThreadSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)
