from django.db import models
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType


class AbstractMetaDataModel(models.Model):
    title = models.CharField(max_length=32)
    description = models.CharField(max_length=256, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    status = models.IntegerField(blank=True, default=0)

    class Meta:
        abstract = True


# ALREADY HAS VIEW
#ALREADY HAS SERIALIZER
class Team(AbstractMetaDataModel):
    members = models.ManyToManyField('auth.User', related_name='teams')


#ALREADY HAS VIEW
#ALREADY HAS SERIALIZER
class Project(AbstractMetaDataModel):
    teams = models.ManyToManyField('Team', related_name='projects', null=True, blank=True)
    owner = models.ForeignKey('auth.User', related_name='projects')


class AbstractRootObjectModel(AbstractMetaDataModel):
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE, null=True, blank=True)
    object_id = models.PositiveIntegerField(null=True, blank=True)
    content_object = GenericForeignKey('content_type', 'object_id')

    gasks = GenericRelation('Gask')
    issues = GenericRelation('Issue')
    threads = GenericRelation('Thread')

    class Meta:
        abstract = True


#ALREADY HAS VIEW
#ALREADY HAS SERIALIZER
class Gask(AbstractRootObjectModel):
    project = models.ForeignKey('Project', related_name='gasks', on_delete=models.CASCADE)
    owner = models.ForeignKey('auth.User', related_name='gasks', on_delete=models.CASCADE)
    deadline = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return self.title


#ALREADY HAS VIEW
#ALREADY HAS SERIALIZER
class Issue(AbstractRootObjectModel):
    project = models.ForeignKey('Project', related_name='issues', on_delete=models.CASCADE)
    owner = models.ForeignKey('auth.User', related_name='issues', on_delete=models.CASCADE)


#ALREADY HAS VIEW
#ALREADY HAS SERIALIZER
class Thread(AbstractRootObjectModel):
    project = models.ForeignKey('Project', related_name='threads', on_delete=models.CASCADE)
    owner = models.ForeignKey('auth.User', related_name='threads', on_delete=models.CASCADE)


#ALREADY HAS VIEW
#ALREADY HAS SERIALIZER
class Post(models.Model):
    created_at = models.DateTimeField(auto_now_add=True, blank=True)
    owner = models.ForeignKey('auth.User', related_name='posts', on_delete=models.CASCADE)
    thread = models.ForeignKey('Thread', on_delete=models.CASCADE)
    post_body = models.CharField(max_length=256, blank=True)


#ALREADY HAS VIEW
#ALREADY HAS SERIALIZER
class TimeEntry(models.Model):
    owner = models.ForeignKey('auth.User', related_name='time_entries', on_delete=models.CASCADE)
    parent = models.ForeignKey('Gask', related_name='time_entries', on_delete=models.CASCADE)
    start_time = models.DateTimeField(blank=True, auto_now_add=True)
    end_time = models.DateTimeField(blank=True, null=True)

