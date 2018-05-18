import uuid

from . import RedisBase


class CsrfToken(RedisBase):
    """
    用于防止 CSRF 攻击
    """
    @classmethod
    def new(cls):
        token = uuid.uuid4()
        cls.set(token, None, 7200)
        return token

    @classmethod
    def valid(cls, token):
        return cls.exist(token)
