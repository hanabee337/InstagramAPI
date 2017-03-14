"""
MEDIA 세팅
    MEDIA_URL, MEDIA_ROOT가 제대로 동작하도록 settings.py에 설정
    MEDIA_ROOT는 django_app/media의 위치를 사용
"""
from django.contrib.auth import get_user_model
from django.http import HttpResponse
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from post.models import Post, PostPhoto

User = get_user_model()


def post_list(request):
    """
    JsonResponse를 이용해서 Post.objects.all()에 해당하는 객체 리스트를 리턴해본다.
    """
    # 하기와 같이 할 경우, 아래와 같은 에러 발생함. 따라서, Json 형식으로 변환해줘야 함.
    # <QuerySet [<Post: Post object>, <Post: Post object>]> is not JSON serializable.
    # post = Post.objects.all()
    # context = {
    #     'post_list': post
    # }

    # 그런데, 인스턴스를 바로 Json형식으로 변환하는 것이 안되기 때문에,
    # dict형태로 변환시켜준다.
    # post_list = Post.objects.all()
    # 효율적인 query를 위해 selecte_related 사용
    post_list = Post.objects.select_related('author')
    post_dict_list = []
    # 전체 Post를 loop
    for post in post_list:
        # 각 Photo의 정보
        cur_post_dict = {
            'pk': post.pk,
            'photo_list': [],
            'author': {
                'pk': post.author.pk,
                'username': post.author.username,
            }
        }
        first_photo = post.postphoto_set.first()
        if first_photo:
            first_photo_dict = {
                'pk': first_photo.pk,
                'photo': first_photo.photo.url,
            }
            cur_post_dict['photo_list'] = first_photo_dict

        post_dict_list.append(cur_post_dict)

    context = {
        'post_list': post_dict_list,
    }
    return JsonResponse(data=context)


@csrf_exempt
def post_create(request):
    """
    request.POST로 전달된 author_id를 받아 post를 생성
    이후 생성된 post의 id값을 HttpResponse로 반환

    받은 author_id에 해당하는 MyUser객체를 가져옴
    실패시, 예외처리로 주어진 author_id에 해당하는 User는 없음을 리턴

    urls.py에 연결
        post/urls.py 생성 후,
        config/urls.py에는 include로 연결
    """
    if request.method == 'POST':
        try:
            author_id = request.POST['author_id']
            author = User.objects.get(id=author_id)
        except KeyError:
            return HttpResponse('key "author_id" is required field')
        except User.DoesNotExist:
            return HttpResponse('author_id {} is not exist'.format(
                request.POST['author_id']
            ))

        post = Post.objects.create(author=author)
        return HttpResponse('{}'.format(post.pk))
    else:
        return HttpResponse('Post create view')


@csrf_exempt
def post_photo_add(request):
    """
    post_id, photo를 받아서
    PostPhoto객체를 생성
    이후, post_id와 post에 연결된 photo들의 id값을 리턴

    extra:
        post_id, photo가 request.POST, request.DATA에 존재하는지 예외처리
        전달된 post_id에 해당하는 Post객체가 있는지 예외처리
    """
    if request.method == 'POST':
        try:
            post_id = request.POST['post_id']
            photo = request.FILES['photo']
            post = Post.objects.get(id=post_id)
        except KeyError:
            return HttpResponse('post_id and photo are required fields')
        except Post.DoesNotExist:
            return HttpResponse('post_id {} is not exist'.format(
                request.POST['post_id']
            ))
        PostPhoto.objects.create(
            post=post,
            photo=photo
        )
        return HttpResponse('Post: {}, PhotoList: {}'.format(
            post.id,
            [photo.id for photo in post.postphoto_set.all()]
        ))
    else:
        return HttpResponse('Post photo add view')
