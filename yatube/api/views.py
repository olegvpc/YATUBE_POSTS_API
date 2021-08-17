from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated, SAFE_METHODS
from django.shortcuts import get_object_or_404

from .serializers import CommentSerializer, GroupSerializer, PostSerializer
from posts.models import Group, Post


class IsAuthorOrReadOnly(IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return request.method in SAFE_METHODS or obj.author == request.user


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthorOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    # def perform_update(self, serializer):
    #     if serializer.instance.author != self.request.user:
    #         raise PermissionDenied('Изменение чужого контента запрещено!')
    #     serializer.save()

    # def perform_destroy(self, instance):
    #     if instance.author != self.request.user:
    #         raise PermissionDenied('Изменение чужого контента запрещено!')
    #     instance.delete()


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


# class UserViewSet(viewsets.ReadOnlyModelViewSet):
#     queryset = User.objects.all()
#     serializer_class = UserSerializer


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [IsAuthorOrReadOnly]

    def get_queryset(self):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        return post.comments

    def perform_create(self, serializer):
        post = get_object_or_404(Post, pk=self.kwargs.get('post_id'))
        serializer.save(author=self.request.user, post=post)

    # def perform_update(self, serializer):
    #     if serializer.instance.author != self.request.user:
    #         raise PermissionDenied('Изменение чужого контента запрещено!')
    #     serializer.save()
    #
    # def perform_destroy(self, instance):
    #     if instance.author != self.request.user:
    #         raise PermissionDenied('Изменение чужого контента запрещено!')
    #     instance.delete()
