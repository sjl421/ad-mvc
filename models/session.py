import uuid

from . import RedisBase


class Session(RedisBase):
    """
    用于关联用户和会话
    """
    @classmethod
    def new(cls, user):
        session = uuid.uuid4()
        cls.set(session, user.id, 7200)
        return session

    @classmethod
    def find_user(cls, session):
        from .user import User
        if cls.exist(session):
            user_id = int(cls.get(session))
            u = User.find_by(id=user_id)
            return u
        else:
            return None
