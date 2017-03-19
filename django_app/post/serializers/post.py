from rest_framework import serializers

from post.models import Post
from post.serializers import PostPhotoSerializer

__all__ = (
    'PostSerializer',
)


class PostSerializer(serializers.ModelSerializer):
    author = serializers.PrimaryKeyRelatedField(read_only=True)
    postphoto_set = PostPhotoSerializer(many=True)

    class Meta:
        model = Post
        fields = (
            'pk',
            'author',
            'created_date',
            'postphoto_set',
        )
        read_only_fields = (
            'created_date',
        )
