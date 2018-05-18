import json
from functools import wraps

from models.csrf_token import CsrfToken
from utils import log
from .. import (
    formatted_header,
    current_user,
)


def json_response(data, headers=None):
    """
    本函数返回 json 格式的 body 数据
    前端的 ajax 函数就可以用 JSON.parse 解析出格式化的数据
    """
    h = {
        'Content-Type': 'application/json',
    }

    if headers is None:
        headers = h
    else:
        headers.update(h)

    header = formatted_header(headers)
    body = json.dumps(data, ensure_ascii=False, indent=2)
    r = header + '\r\n' + body

    return r.encode()


def api_error_response(error):
    """
    ajax 无法直接 redirect，故约定在失败时添加一个 error 字段作为标记
    """
    d = dict(error=error)
    return json_response(d)


def api_login_required(route_function):
    @wraps(route_function)
    def wrapper(request):
        u = current_user(request)
        if u.is_guest():
            return api_error_response('请先登录')
        else:
            return route_function(request)

    return wrapper


def api_csrf_required(route_function):
    @wraps(route_function)
    def wrapper(request):
        token = request.query['csrf_token']

        if CsrfToken.valid(token):
            # ajax 不刷新页面，不会产生新 token
            # 故不删除当前 token
            return route_function(request)
        else:
            return api_error_response('Token 无效，请尝试刷新页面')

    return wrapper
