from django.shortcuts import render

# Create your views here.
from django.shortcuts import get_object_or_404, render
from rest_framework import generics, serializers, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import (IsAuthenticated,
                                        IsAuthenticatedOrReadOnly, AllowAny)
from rest_framework.response import Response
from authors.apps.article.models import Article
from .models import Comment
from .renderer import (CommentJSONRenderer, CommentThreadJSONRenderer)
from .serializers import CommentSerializer, CommentChildSerializer


class CommentCreateListView(generics.ListCreateAPIView):
    """

    create comments and retrieve comments 

    """
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated, )
    renderer_classes = (CommentJSONRenderer, )
    queryset = Comment.objects.all().filter()
    lookup_field = 'slug'

    def post(self, request, *args, **kwargs):
        """
        This method posts a comment to article
        """
        article_slug = self.kwargs['slug']
        slug = get_object_or_404(Article, slug=article_slug)
        comment = request.data.get('comment', {})
        serializer = self.serializer_class(data=comment, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(commented_by=self.request.user, slug=slug)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request, *args, **kwargs):

        article_slug = self.kwargs['slug']
        slug = get_object_or_404(Article, slug=article_slug)  # findout
        comment = self.queryset.filter(slug=article_slug)
        serializer = self.serializer_class(comment, many=True)
        return Response(serializer.data)


class CommentsAPIView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated, )
    renderer_classes = (CommentJSONRenderer, )
    lookup_fields = 'id', 'slug'
    queryset = Comment.objects.all().filter(parent__isnull=True)

    def destroy(self, request, *args, **kwargs):
        article_slug = self.kwargs['slug']
        slug = get_object_or_404(Article, slug=article_slug)
        instance = self.get_object()
        #raise Exception(instance)
        self.check_user(instance, request)
        self.perform_destroy(instance)
        return Response({
            "message": "This comment has been deleted successfully"
        },
                        status=status.HTTP_200_OK)

    def check_user(self, instance, request):
        if instance.commented_by != request.user:
            raise PermissionDenied

    def get_object(self):
        queryset = self.get_queryset()
        # Get the base queryset
        # queryset = self.filter_queryset(queryset)  # Apply any filter backends
        filter = {}
        for field in self.lookup_fields:
            filter[field] = self.kwargs[field]
        return get_object_or_404(queryset, **filter)


class CommentsListThreadsCreateView(generics.RetrieveAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = CommentChildSerializer
    renderer_classes = (CommentThreadJSONRenderer, )
    lookup_fields = 'id', 'slug'
    queryset = Comment.objects.all().filter(parent__isnull=False)

    def post(self, request, *args, **kwargs):
        article_slug = self.kwargs['slug']
        slug = get_object_or_404(Article, slug=article_slug)
        thread = request.data.get('comment', {})
        thread['parent'] = self.kwargs['id']
        serializer = self.serializer_class(data=thread, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save(commented_by=self.request.user, slug=slug)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def get(self, request, *args, **kwargs):
        article_slug = self.kwargs['slug']
        slug = get_object_or_404(Article, slug=article_slug)
        comment = self.queryset.filter(
            slug=article_slug, parent=self.kwargs['id'])
        serializer = self.serializer_class(comment, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)