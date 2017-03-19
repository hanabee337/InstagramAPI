from rest_framework import generics

from post.models import Post
from post.serializers import PostPhotoSerializer

__all__ = (
    'PostPhotoCreate',
    'PostPhotoDestroy',
)


class PostPhotoCreate(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostPhotoSerializer


class PostPhotoDestroy(generics.DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostPhotoSerializer
