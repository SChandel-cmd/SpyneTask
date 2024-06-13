from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

router = DefaultRouter()
router.register(r'users', UserViewSet)
router.register(r'discussions', DiscussionViewSet)
router.register(r'follows', FollowViewSet, basename='follow')
router.register(r'comments', CommentViewSet)
router.register(r'likes', LikeViewSet)
router.register(r'commentlikes', CommentLikeViewSet)
router.register(r'replies', ReplyViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('token/', CustomTokenObtainView.as_view(), name='token_obtain_pair'),
    path('users/search', UserSearchView.as_view(), name='user_search'),
    path('users/update/<int:pk>', UserUpdateView.as_view(), name='user_update'),
    path('users/delete/<int:pk>', UserDeleteView.as_view(), name='user_delete'),
    path('discussions/update/<int:pk>', DiscussionUpdateView.as_view(), name='discussion_update'),
    path('discussions/delete/<int:pk>', DiscussionDeleteView.as_view(), name='discussion_delete'),
    path('discussions/search', DiscussionListView.as_view(), name='discussion_search'),
    path('users/followers/<int:user_id>', FollowersListView.as_view({'get': 'list'}), name='user-followers'),
    path('users/following/<int:user_id>', FollowingListView.as_view({'get': 'list'}), name='user-following'),
]
