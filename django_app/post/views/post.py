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

Mission 4.
    - Bower 설치
        1. bower install(django_app 폴더에서)
            $ curl -sL https://deb.nodesource.com/setup_6.x | sudo -E bash -
            $ sudo apt-get install nodejs
            $ sudo npm install -g bower
            $ bower -version
            $ bower init
            $ bower install jquery
            $ bower install swiper
        2. .gitignore에 bower_components 추가
"""
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import DeleteView
from django.views.generic import DetailView
from django.views.generic import FormView
from django.views.generic import ListView

from post.forms import PostForm
from post.models import Post
from post.models import PostComment
from post.models import PostPhoto

__all__ = (
    'PostList',
    'PostDetail',
    'PostDelete',
    'PostCreate',
)


# funcion-based view였다면, 아래와 같았을 것이다.
# def post_list(request):
#     pass


class PostList(ListView):
    """
    2017.03.20
    Mission 3.
        1. 데이터추가
            Postman으로 Post두개 만들고, 각각의 Post에 PostPhoto를 3개 추가
        2. post_list.html에서 posts변수를 loop하며 각 post의 postphoto_set.all을 loop
            postphoto_set을 내부에서 loop하며 내부 loop아이템의 photo.url을 이용해 이미지를 출력
    """
    model = Post
    context_object_name = 'posts'


class PostDetail(DetailView):
    """
    2017.03.20
    Mission 5.
        하나의 Post object를 리턴해서 받는 view 구현
        DetailView를 상속받아서 구현되도록 해보세요
    """
    model = Post


class PostCreate(FormView):
    """
    2017.03.21
    Mission 1.
        PostForm을 사용
            fields
                content
                photos
    Mission 2.
        Post 요청을 받았을 때,
        1. 해당 request.user를 author로 하는 Post 인스턴스 생성
        2. 만약 form.cleaned_data['content']가 빈 값이 아니면 PostComment 인스턴스 생성
        3. request.FILES.getlist('photos')를 loop하며 PostPhoto 인스턴스 생성
        4. return redirect('post:post-list')

    Mission 3.
        FormView를 상속받아  구현

        attributes
            template_name
            form_class
            success_url

        method
            form_valid(self, form)
                request는 self.request로 접근 가능
                form.cleaned_data는 바로 사용 가능
                redirect는 정의해줄 필요 없음
    """
    form_class = PostForm
    template_name = 'post/post_create.html'

    # def get(self, request, *args, **kwargs):
    #     form = self.form_class()
    #     context = {
    #         'form': form,
    #     }
    #     return render(request, self.template_name, context)
    #
    # def post(self, request, *args, **kwargs):
    #     post = Post.objects.create(author=request.user)
    #
    #     form = self.form_class(request.POST, request.FILES)
    #     if form.is_valid():
    #         content = form.cleaned_data.get('content', '').strip()
    #         if content != '':
    #             PostComment.objects.create(
    #                 author=request.user,
    #                 post=post,
    #                 content=content,
    #             )
    #
    #         # print(request.POST)
    #         # print(request.FILES)
    #         # print(content)
    #
    #         for file in request.FILES.getlist('photos'):
    #             PostPhoto.objects.create(
    #                 post=post,
    #                 photo=file,
    #             )
    #         return redirect('post:post-list')
    #     else:
    #         return HttpResponse(form.errors)

    success_url = '/post/list/'

    def form_valid(self, form):
        post = Post.objects.create(author=self.request.user)
        content = form.cleaned_data.get('content', '').strip()
        if content != '':
            PostComment.objects.create(
                author=self.request.user,
                post=post,
                content=content,
            )
            for file in self.request.FILES.getlist('photos'):
                PostPhoto.objects.create(
                    post=post,
                    photo=file,
                )
        return super().form_valid(form)


class PostDelete(DeleteView):
    """
    2017.03.21
    Mission 4.
        DeleteView를 상속받아 구현해보세요
    """
    model = Post

    success_url = reverse_lazy('post:post-list')
