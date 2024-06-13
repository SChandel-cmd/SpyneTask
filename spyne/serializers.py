from rest_framework import serializers
from .models import User, Discussion, Follow, Comment, Like, CommentLike, Reply
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from django.contrib.auth.hashers import make_password

class CustomTokenObtainSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')

        user = authenticate(email=email, password=password)
        if user is None:
            raise serializers.ValidationError('Invalid login credentials')

        refresh = RefreshToken.for_user(user)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        }

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'name', 'mobile', 'email', 'password']
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        instance = super().update(instance, validated_data)
        if password:
            instance.password = make_password(password)
            instance.save()
        return instance

class FollowSerializer(serializers.ModelSerializer):
    follower = UserSerializer(read_only=True)
    following = UserSerializer(read_only=True)

    class Meta:
        model = Follow
        fields = ['id', 'follower', 'following', 'created_at']

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'user', 'discussion', 'text', 'created_on']
        read_only_fields = ['user']

    def create(self, validated_data):
        user = self.context['request'].user
        comment = Comment.objects.create(user=user, **validated_data)
        return comment

class DiscussionSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True, read_only=True)
    likes = serializers.IntegerField(source='likes.count', read_only=True)

    class Meta:
        model = Discussion
        fields = ['id', 'user', 'text', 'image', 'hashtags', 'created_on', 'views', 'likes', 'comments']
        read_only_fields = ['user', 'views']

    def create(self, validated_data):
        user = self.context['request'].user
        discussion = Discussion.objects.create(user=user, **validated_data)
        return discussion

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ['id', 'user', 'discussion', 'created_on']
        read_only_fields = ['user']

    def create(self, validated_data):
        user = self.context['request'].user
        like = Like.objects.create(user=user, **validated_data)
        return like

class CommentLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentLike
        fields = ['id', 'user', 'comment', 'created_on']
        read_only_fields = ['user']

    def create(self, validated_data):
        user = self.context['request'].user
        comment_like = CommentLike.objects.create(user=user, **validated_data)
        return comment_like

class ReplySerializer(serializers.ModelSerializer):
    class Meta:
        model = Reply
        fields = ['id', 'user', 'comment', 'text', 'created_on']
        read_only_fields = ['user']

    def create(self, validated_data):
        user = self.context['request'].user
        reply = Reply.objects.create(user=user, **validated_data)
        return reply
