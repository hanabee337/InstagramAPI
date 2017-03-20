"""
2017.03.20
Mission 1.
    - Class-based View로
        PostList, PostDetail, PostCreate, PostDelete view를 작성
        (내용 없음)
"""
from django.views import View


# funcion-based view였다면, 아래와 같았을 것이다.
# def post_list(request):
#     pass

class PostList(View):
    pass


class PostDetail(View):
    pass


class PostDelete(View):
    pass
