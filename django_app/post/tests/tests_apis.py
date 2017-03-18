from django.contrib.auth import get_user_model
from django.urls import NoReverseMatch
from django.urls import resolve
from django.urls import reverse
from django.utils.crypto import random
from rest_framework import status
from rest_framework.test import APILiveServerTestCase

from post.models import Post

User = get_user_model()


class PostTest(APILiveServerTestCase):
    test_username = 'test_username'
    test_password = 'test_password'

    def create_user(self):
        user = User.objects.create_user(
            username=self.test_username,
            password=self.test_password,
        )
        return user

    def create_user_and_login(self):
        self.create_user()
        self.client.login(
            username=self.test_username,
            password=self.test_password,
        )

    def create_post(self, num=1):
        """
        :param num: 생성할 Post수
        :return: num == 1일 경우, 생성 요청의 response
        """

        # Post를 생성하는 API주소를 reverse
        url = reverse('api:post-list')
        # Post를 생성하는 API주소에 POST요청, response를 받아옴
        for i in range(num):
            response = self.client.post(url)
            if num == 1:
                return response

    def test_apis_url_exist(self):
        try:
            # PostList
            resolve('/api/post/')

            # PostDetail
            resolve('/api/post/1/')
        except NoReverseMatch as e:
            self.fail(e)

    def test_post_create(self):
        # Post를 만들 유저를 생성 및 로그인
        user = self.create_user()
        self.client.login(
            username=self.test_username,
            password=self.test_password,
        )

        # Post 생성
        response = self.create_post()

        # response의 status_code가 201(Created)이어야 함
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # response의 key값 검사
        self.assertIn('author', response.data)
        self.assertIn('created_date', response.data)

        # 생성 후 Post인스턴스가 총 1개여야 함
        self.assertEqual(Post.objects.count(), 1)

        # 생성된 Post인스턴스의 author pk(id)가 테스트시 생성한 User의 pk(id)와 같아야 함
        post = Post.objects.first()
        self.assertEqual(post.author.id, user.id)

    def test_cannot_create_post_not_authenticated(self):
        url = reverse('api:post-list')
        print('url: {}'.format(url))
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(Post.objects.exists(), False)

    def test_post_list(self):
        # Post 생성 위해 유저 생성 후 로그인
        self.create_user_and_login()

        # 생성할 Post 개수 지정
        num = random.randrange(1, 50)

        # num만큼 Post 생성
        self.create_post(num)

        # Post를 생성하는 API주소를 reverse
        url = reverse('api:post-list')

        # Post를 생성하는 API주소에 GET요청, response를 받아옴
        response = self.client.get(url)
        # print(response.data)

        # status_code 확인
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # num만큼 생성되었는지 확인
        self.assertEqual(len(response.data), num)

    def test_post_update(self):
        pass

    def test_post_partial_update(self):
        pass

    def test_post_retrieve(self):
        pass

    def test_post_destroy(self):
        pass
