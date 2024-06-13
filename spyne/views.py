from rest_framework import viewsets, generics, status, permissions
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import User, Discussion, Follow, Comment, Like, CommentLike, Reply
from .serializers import CustomTokenObtainSerializer, UserSerializer, DiscussionSerializer, FollowSerializer, CommentSerializer, LikeSerializer, CommentLikeSerializer, ReplySerializer
from .permissions import IsOwner
from .filters import HashtagAndTextFilter

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.user == request.user
class CustomTokenObtainView(APIView):
    def post(self, request, *args, **kwargs):
        serializer = CustomTokenObtainSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserSearchView(generics.ListAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        queryset = User.objects.all()
        name = self.request.query_params.get('name', None)
        if name is not None:
            queryset = queryset.filter(name__icontains=name)
        return queryset

class UserUpdateView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated]

class UserDeleteView(generics.DestroyAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.IsAuthenticated]
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance_id = instance.id
        self.perform_destroy(instance)
        return Response({'id': instance_id, 'message': 'User deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

class FollowViewSet(viewsets.ModelViewSet):
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]
    def create(self, request, *args, **kwargs):
        following_id = request.data.get('following_id')
        if not following_id:
            return Response({'error': 'following_id is required'}, status=status.HTTP_400_BAD_REQUEST)

        following_user = User.objects.get(id=following_id)
        follow, created = Follow.objects.get_or_create(follower=request.user, following=following_user)

        if not created:
            return Response({'error': 'You are already following this user'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = self.get_serializer(follow)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk=None):
        following_id = pk
        follower_id = request.user.id
        follow = Follow.objects.get(following_id=following_id, follower_id=follower_id)
        if follow.follower != request.user:
            return Response({'error': 'You cannot unfollow this user'}, status=status.HTTP_403_FORBIDDEN)
        self.perform_destroy(follow)
        return Response({'id': following_id, 'message': 'User unfollowed successfully'}, status=status.HTTP_204_NO_CONTENT)

class FollowersListView(viewsets.ReadOnlyModelViewSet):
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        user_id = self.kwargs['user_id']
        followers = Follow.objects.filter(following_id=user_id)
        follower_users = [
            {
                'id': follow.following.id,
                'name': User.objects.filter(id=user_id).first().name
            }
            for follow in followers
        ]
        return Response(follower_users, status=status.HTTP_200_OK)

class FollowingListView(viewsets.ReadOnlyModelViewSet):
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]

    def list(self, request, *args, **kwargs):
        user_id = self.kwargs['user_id']
        following = Follow.objects.filter(follower_id=user_id)
        following_users = [
            {
                'id': follow.follower.id,
                'name': User.objects.filter(id=user_id).first().name
            }
            for follow in following
        ]
        return Response(following_users, status=status.HTTP_200_OK)

class DiscussionViewSet(viewsets.ModelViewSet):
    queryset = Discussion.objects.all()
    serializer_class = DiscussionSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def retrieve(self, request, pk=None):
        try:
            discussion = Discussion.objects.get(pk=pk)
            discussion.views += 1
            discussion.save()
            serializer = DiscussionSerializer(discussion)
            return Response(serializer.data)
        except Discussion.DoesNotExist:
            return Response({'error': 'Discussion not found'}, status=404)

        return 0


class DiscussionUpdateView(generics.UpdateAPIView):
    queryset = Discussion.objects.all()
    serializer_class = DiscussionSerializer
    permission_classes = [IsOwner]
    def put(self, request, *args, **kwargs):
        response = super().put(request, *args, **kwargs)
        updated_data = response.data
        return Response(updated_data, status=response.status_code)

class DiscussionDeleteView(generics.DestroyAPIView):
    queryset = Discussion.objects.all()
    permission_classes = [IsOwner]
    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        instance_id = instance.id
        self.perform_destroy(instance)
        return Response({'id': instance_id, 'message': 'Discussion deleted successfully'}, status=status.HTTP_204_NO_CONTENT)

class DiscussionListView(generics.ListAPIView):
    queryset = Discussion.objects.all()
    serializer_class = DiscussionSerializer
    filter_backends = [HashtagAndTextFilter]

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        data = request.data.copy()
        data['discussion'] = instance.discussion.id
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance_id = instance.id
        self.perform_destroy(instance)
        return Response({'id': instance_id, 'message': 'Comment deleted successfully'},
                        status=status.HTTP_204_NO_CONTENT)


class LikeViewSet(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request):
        user = request.user
        discussion_id = request.data.get('discussion')

        if not discussion_id:
            return Response({'error': 'Discussion ID is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            discussion = Discussion.objects.get(id=discussion_id)
        except Discussion.DoesNotExist:
            return Response({'error': 'Discussion not found'}, status=status.HTTP_404_NOT_FOUND)

        if Like.objects.filter(discussion=discussion, user=user).exists():
            return Response({'error': 'You have already liked this discussion'}, status=status.HTTP_400_BAD_REQUEST)

        like = Like(discussion=discussion, user=user)
        like.save()
        serializer = LikeSerializer(like)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def destroy(self, request, pk=None):
        user = request.user
        try:
            like = Like.objects.get(discussion_id=pk, user=user)
            like.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Like.DoesNotExist:
            return Response({'error': 'Like not found'}, status=status.HTTP_404_NOT_FOUND)

class CommentLikeViewSet(viewsets.ModelViewSet):
    queryset = CommentLike.objects.all()
    serializer_class = CommentLikeSerializer
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

class ReplyViewSet(viewsets.ModelViewSet):
    queryset = Reply.objects.all()
    serializer_class = ReplySerializer
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        data = request.data.copy()
        data['comment'] = instance.comment.id
        serializer = self.get_serializer(instance, data=data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        return Response(serializer.data)

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        instance_id = instance.id
        self.perform_destroy(instance)
        return Response({'id': instance_id, 'message': 'Reply deleted successfully'},
                        status=status.HTTP_204_NO_CONTENT)
