from rest_framework import serializers
from gaskserv.models import *
from django.contrib.auth.models import User
from rest_framework.validators import UniqueValidator


class ContentTypeField(serializers.Field):
    def to_internal_value(self, data):
        if data:
            return ContentType.objects.get(model=data)
        pass

    def to_representation(self, value):
        return value.model

class AbstractMetaDataSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('title', 'status', 'description', 'created_at')


class ProjectSerializer(AbstractMetaDataSerializer):
    # gasks = serializers.PrimaryKeyRelatedField(many=True, queryset=Gask.objects.exclude(object_id__isnull=False))
    # issues = serializers.PrimaryKeyRelatedField(many=True, queryset=Issue.objects.exclude(object_id__isnull=False))
    # threads = serializers.PrimaryKeyRelatedField(many=True, queryset=Thread.objects.exclude(object_id__isnull=False))
    owner = serializers.ReadOnlyField(source='owner.username')

    gasks = serializers.SerializerMethodField()
    issues = serializers.SerializerMethodField()
    threads = serializers.SerializerMethodField()

    def get_gasks(self, obj):

        return Gask.objects.filter(project=obj).exclude(object_id__isnull=False).values_list('pk', flat=True)

    def get_issues(self, obj):
        return Issue.objects.filter(project=obj).exclude(object_id__isnull=False).values_list('pk', flat=True)

    def get_threads(self, obj):
        return Thread.objects.filter(project=obj).exclude(object_id__isnull=False).values_list('pk', flat=True)

    class Meta:
        model = Project
        fields = AbstractMetaDataSerializer.Meta.fields + ('id', 'gasks', 'issues', 'threads', 'owner', 'teams')


class TimeEntrySerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = TimeEntry
        fields = ('start_time', 'end_time', 'parent', 'owner', 'id')


class UserSerializer(serializers.ModelSerializer):
    gasks = serializers.PrimaryKeyRelatedField(many=True, queryset=Gask.objects.all())
    email = serializers.EmailField(validators=[UniqueValidator(queryset=User.objects.all())])

    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email', 'gasks', 'first_name', 'last_name', 'time_entries')
        extra_kwargs = {
            'password': {'write_only': True},
            'gasks': {'read_only': True}
        }

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user


class GaskRelatedField(serializers.RelatedField):
    def to_representation(self, value):

        if isinstance(value, Gask):
            return GaskSerializer(value).data

        elif isinstance(value, Issue):
            return IssueSerializer(value).data

        elif isinstance(value, Thread):
            return ThreadSerializer(value).data

        elif isinstance(value, TimeEntry):
            return TimeEntrySerializer(value).data

        else:
            raise Exception('UnexpectedTypeToSerialize')



class AbstractRootObjectSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    gasks = serializers.PrimaryKeyRelatedField(many=True, queryset=Gask.objects.all())
    issues = serializers.PrimaryKeyRelatedField(many=True, queryset=Issue.objects.all())
    threads = serializers.PrimaryKeyRelatedField(many=True, queryset=Thread.objects.all())
    content_type = ContentTypeField()

    class Meta:
        fields = ('owner', 'id', 'status', 'title', 'description', 'created_at', 'gasks', 'issues', 'threads', 'project', 'content_type', 'object_id')


class GaskSerializer(AbstractRootObjectSerializer):
    time_entries = GaskRelatedField(many=True, read_only=True)

    class Meta:
        model = Gask
        fields = AbstractRootObjectSerializer.Meta.fields + ('deadline', 'time_entries')


class IssueSerializer(AbstractRootObjectSerializer):
    class Meta:
        model = Issue
        fields = AbstractRootObjectSerializer.Meta.fields


class ThreadSerializer(AbstractRootObjectSerializer):
    class Meta:
        model = Thread
        fields = AbstractRootObjectSerializer.Meta.fields


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('owner', 'created_at', 'thread', 'post_body')


class TeamSerializer(AbstractMetaDataSerializer):
    projects = serializers.PrimaryKeyRelatedField(many=True, queryset=Project.objects.all())

    class Meta:
        model = Team
        fields = AbstractMetaDataSerializer.Meta.fields + ('projects', 'members')