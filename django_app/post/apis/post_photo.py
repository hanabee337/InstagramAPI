from rest_framework import generics

from post.models import Post

__all__ = (
    'PostPhotoCreate',
    'PostPhotoDestroy',
)


class PostPhotoCreate(generics.CreateAPIView):
    queryset = Post.objects.all()


class PostPhotoDestroy(generics.DestroyAPIView):
    queryset = Post.objects.all()
