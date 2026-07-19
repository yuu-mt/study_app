import base64

from django.conf import settings
from django.http import HttpResponse


class DemoBasicAuthMiddleware:
    """クライアントへのデモ公開時など、一時的にAPI全体へアクセス制限をかけるためのミドルウェア。

    環境変数 DEMO_AUTH_USER / DEMO_AUTH_PASSWORD の両方が設定されている場合のみ有効になる。
    フロントエンド（Vercel Edge Middleware）と同じ認証情報を設定することで、
    フロントエンド・バックエンドの両方をまとめて非公開にできる。
    不要になったら環境変数を削除するだけで解除できる（コードの変更は不要）。
    """

    def __init__(self, get_response):
        self.get_response = get_response
        self.user = getattr(settings, 'DEMO_AUTH_USER', None)
        self.password = getattr(settings, 'DEMO_AUTH_PASSWORD', None)

    def __call__(self, request):
        if not self.user or not self.password:
            return self.get_response(request)

        auth_header = request.META.get('HTTP_AUTHORIZATION', '')
        if auth_header.startswith('Basic '):
            try:
                decoded = base64.b64decode(auth_header.split(' ', 1)[1]).decode('utf-8')
                input_user, input_password = decoded.split(':', 1)
            except (ValueError, UnicodeDecodeError):
                input_user, input_password = None, None

            if input_user == self.user and input_password == self.password:
                return self.get_response(request)

        response = HttpResponse('Authentication required', status=401)
        response['WWW-Authenticate'] = 'Basic realm="Monster Study Tracker (Preview)"'
        return response
