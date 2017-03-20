"""
2017.03.20
Mission 1.
    - Class-based View로
        PostList, PostDetail, PostCreate, PostDelete view를 작성
        (내용 없음)

Mission 2.
    - 기존 프로젝트의 설정 가져와서 PostList가 작동하도록 구현
        1. settings.py
            STATIC_DIR
                경로 변수 지정
            STATICFILES_DIRS
                STATIC_DIR 을 포함하는 tuple or list로 변수 할당
        2. 기존 프로젝트의 static 폴더 통째로 복사해오기
        3. .gitignore에 django_app/static/css/ 추가
            (CSS 파일은 더 이상 소스코드에 포함되지 않음. SCSS파일만 포함)
        4. 기존 프로젝트의 templates 폴더 통째로 복사
        5. PostList CBV에 get method 작성 및 내부 query 리턴
            (django CBV 문서 보면서 진행)
"""
from django.shortcuts import render
from django.views import View

from post.models import Post

__all__ = (
    'PostList',
    'PostDetail',
    'PostDelete',
)


# funcion-based view였다면, 아래와 같았을 것이다.
# def post_list(request):
#     pass


class PostList(View):
    """
    Mission 3.
        1. 데이터추가
            Postman으로 Post두개 만들고, 각각의 Post에 PostPhoto를 3개 추가
        2. post_list.html에서 posts변수를 loop하며 각 post의 postphoto_set.all을 loop
            postphoto_set을 내부에서 loop하며 내부 loop아이템의 photo.url을 이용해 이미지를 출력
    """
    def get(self, request):
        posts = Post.objects.all()
        context = {
            'posts': posts
        }
        return render(request, 'post/post_list.html', context)


class PostDetail(View):
    """
    하나의 Post object를 리턴해서 받는 view 구현
    """
    pass


class PostDelete(View):
    pass