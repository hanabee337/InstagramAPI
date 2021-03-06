import os

from django.urls import NoReverseMatch
from django.urls import resolve
from django.urls import reverse
from django.utils.crypto import random
from rest_framework import status
from rest_framework.test import APILiveServerTestCase

from post.models import Post
from utils.testcase import APITestCaseAuthMixin


class PostTest(APITestCaseAuthMixin, APILiveServerTestCase):
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
        self.assertIn('postphoto_set', response.data)

        # response의 postphoto_set값 검사
        response_postphoto_set = response.data['postphoto_set']
        self.assertIsInstance(response_postphoto_set, list)
        for postphoto_object in response_postphoto_set:
            self.assertIn('pk', postphoto_object)
            self.assertIn('photo', postphoto_object)
            self.assertIn('created_date', postphoto_object)

        # response의 author 값 검사
        response_author = response.data['author']
        self.assertIn('pk', response_author)
        self.assertIn('username', response_author)

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
        self.create_user_and_login(self.client)

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

        # 생성된 response의 author 필드가 pk가 아닌 dict 형태로 전달되는지 확인
        for item in response.data:
            self.assertIn('author', item)
            self.assertIn('pk', item['author'])
            self.assertIn('username', item['author'])

            # response의 postphoto_set값 검사
            item_postphoto_set = item['postphoto_set']
            self.assertIsInstance(item_postphoto_set, list)
            for postphoto_object in item_postphoto_set:
                self.assertIn('pk', postphoto_object)
                self.assertIn('photo', postphoto_object)
                self.assertIn('created_date', postphoto_object)

    def test_post_update(self):
        pass

    def test_post_partial_update(self):
        pass

    def test_post_retrieve(self):
        pass

    def test_post_destroy(self):
        pass


class PostPhotoTest(APITestCaseAuthMixin, APILiveServerTestCase):
    def test_photo_add_to_post(self):
        # 유저 생성 및 로그인
        user = self.create_user_and_login(self.client)

        # 해당 유저로 Post 생성
        url = reverse('api:post-list')
        response = self.client.post(url)
        print(response.data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Post.objects.count(), 1)
        post = Post.objects.first()
        self.assertEqual(post.author, user)

        # 생성한 Post에 PostPhoto를 추가
        url = reverse('api:photo-create')

        file_path = os.path.join(os.path.dirname(__file__), 'test_image.jpg')
        with open(file_path, 'rb') as fp:
            data = {
                'post': post.id,
                'photo': fp,
            }
            response = self.client.post(url, data)
            print(response.status_code)
            print(response.data)

        # status_code 확인
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # key 확인
        self.assertIn('post', response.data)
        self.assertIn('photo', response.data)

        # value 확인
        self.assertEqual(post.pk, response.data['post'])

    def test_cannot_photo_add_to_post_not_authenticated(self):
        pass

    def test_cannot_photo_add_to_post_user_is_not_author(self):
        pass
