import json
import os
import uuid

import redis

import config
from utils import log
from .user_role import (
    JsonEncoder,
    json_decode,
)


def save(data, path):
    """
    本函数把一个 dict 或者 list 写入文件
    data 是 dict 或者 list
    path 是保存文件的路径
    """
    s = json.dumps(data, indent=2, ensure_ascii=False, cls=JsonEncoder)
    # 确保目录存在
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w+', encoding='utf-8') as f:
        log('save', path, s, data)
        f.write(s)


def load(path):
    """
    本函数从一个文件中载入数据并转化为 dict 或者 list
    path 是保存文件的路径
    """
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            s = f.read()
            log('load', s)
            return json.loads(s, object_hook=json_decode)
    else:
        log('db not found <{}>'.format(path))
        return []


class Model(object):
    """
    Model 是所有 model 的基类
    """

    def __init__(self, form):
        self.id = form.get('id', None)

    def __repr__(self):
        classname = self.__class__.__name__
        properties = ['{}: ({})'.format(k, v) for k, v in self.__dict__.items()]
        s = '\n'.join(properties)
        return '< {}\n{} >\n'.format(classname, s)

    @classmethod
    def db_path(cls):
        path = 'data/{}.txt'.format(cls.__name__)
        return path

    @classmethod
    def new(cls, form):
        m = cls(form)
        m.save()
        return m

    @classmethod
    def delete(cls, id):
        ms = cls.all()
        for i, m in enumerate(ms):
            if m.id == id:
                del ms[i]
                break

        l = [m.__dict__ for m in ms]
        save(l, cls.db_path())

    @classmethod
    def all(cls):
        path = cls.db_path()
        models = load(path)
        log('models in all', models)

        ms = [cls(m) for m in models]
        return ms

    @classmethod
    def find_by(cls, **kwargs):
        log('find_by kwargs', kwargs)

        for m in cls.all():
            exist = True
            for k, v in kwargs.items():
                if not hasattr(m, k) or not getattr(m, k) == v:
                    exist = False
            if exist:
                return m

    @classmethod
    def find_all(cls, **kwargs):
        log('find_all kwargs', kwargs)
        models = []

        for m in cls.all():
            exist = True
            for k, v in kwargs.items():
                if not hasattr(m, k) or not getattr(m, k) == v:
                    exist = False
            if exist:
                models.append(m)

        return models

    def save(self):
        """
        用 all 方法读取文件中的所有 model 并生成一个 list
        把 self 添加进去并且保存进文件
        """
        models = self.all()
        log('models', models)

        if self.id is None:
            # 加上 id
            if len(models) > 0:
                # 不是第一个元素
                self.id = models[-1].id + 1
            else:
                # 第一个元素
                self.id = 0
            models.append(self)
        else:
            # 有 id 说明已经是存在于数据文件中的数据
            # 那么就找到这条数据并替换
            for i, m in enumerate(models):
                if m.id == self.id:
                    models[i] = self

        l = [m.__dict__ for m in models]
        save(l, self.db_path())

    def json(self):
        """
        返回当前 model 的字典表示
        """
        d = self.__dict__
        return d

    @classmethod
    def all_json(cls):
        ms = cls.all()
        js = [t.json() for t in ms]
        return js


def initialized_redis_connection():
    r = redis.Redis(host='localhost', port=6379, decode_responses=True)
    return r


class RedisBase(object):
    connection = initialized_redis_connection()
    prefix = config.redis_prefix

    @classmethod
    def name_for_key(cls, key):
        name = '{}:{}:{}'.format(cls.prefix, cls.__name__, key)
        return name

    @classmethod
    def set(cls, key, value, time=None):
        """
        time 过期时间（秒）
        """
        name = cls.name_for_key(key)
        cls.connection.set(name, value, ex=time)

    @classmethod
    def get(cls, key, default_value=None):
        name = cls.name_for_key(key)
        v = cls.connection.get(name)
        return v if v is not None else default_value

    @classmethod
    def exist(cls, key):
        name = cls.name_for_key(key)
        return cls.connection.exists(name)

    @classmethod
    def delete(cls, *keys):
        names = (cls.name_for_key(key) for key in keys)
        cls.connection.delete(*names)


class RedisUserMixin(object):
    @classmethod
    def add_user(cls, user):
        id = uuid.uuid4()
        cls.set(id, user.id, 3600)
        return id

    @classmethod
    def user(cls, id):
        from .user import User
        if cls.exist(id):
            user_id = int(cls.get(id))
            u = User.find_by(id=user_id)
            return u if u is not None else User.guest()
        else:
            return User.guest()
