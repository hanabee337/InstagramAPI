from rest_framework import permissions
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

__all__ = (
    'DeleteToken',
)


class DeleteToken(APIView):
    """
    2017.03.22
    H/W
    POST 요청이 오면, request.user가 인증되어 있는 경우, request.auth의 Token을 삭제
    """
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request, format=None):
        # print(request.auth)
        # print(type(request.auth))
        # cur_token = Token.objects.get(ket=request.auth.key)
        # print(cur_token)
        request.auth.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
