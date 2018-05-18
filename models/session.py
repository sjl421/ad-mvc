from . import (
    RedisBase,
    RedisUserMixin,
)


class Session(RedisBase, RedisUserMixin):
    """
    用于关联用户和会话
    """
    pass
