from django.db import models

from config import settings


class Post(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL)
    created_date = models.DateTimeField(auto_now_add=True)

    def to_dict(self):
        """
        post 객체 한 개에 대해서 인스턴스해서 dict형태로 바꿔주는 메서드
        """
        ret = {
            'pk': self.pk,
            'created_date': self.created_date,
            'author': self.author.to_dict(),
            'photo_list': [photo.to_dict() for photo in self.postphoto_set.all()]
        }
        return ret


class PostPhoto(models.Model):
    post = models.ForeignKey(Post)
    photo = models.ImageField(upload_to='post')

    class Meta:
        order_with_respect_to = 'post'

    def to_dict(self):
        ret = {
            'pk': self.pk,
            'photo': self.photo.url,
        }
        return ret
