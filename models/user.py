import hashlib

from . import Model


class User(Model):
    """
    User 是一个保存用户数据的 model
    现在只有两个属性 username 和 password
    """
    def __init__(self, form):
        super().__init__(form)
        self.username = form['username']
        self.password = form['password']

    @classmethod
    def guest(cls):
        form = dict(
            username='游客',
            password='',
        )
        g = cls(form)
        return g

    def is_guest(self):
        return self.id is None

    @staticmethod
    def salted_password(password, salt='$!@><?>HUI&DWQa`'):
        salted = password + salt
        hashed = hashlib.sha256(salted.encode('ascii')).hexdigest()
        return hashed

    @classmethod
    def login(cls, form):
        salted = cls.salted_password(form['password'])
        u = User.find_by(username=form['username'], password=salted)

        if u is not None:
            result = '登录成功'
        else:
            result = '用户名或者密码错误'

        return u, result

    @classmethod
    def register(cls, form):
        username = form['username']
        password = form['password']
        valid = len(username) > 2 and len(password) > 2

        if valid:
            u = cls.find_by(username=username)
            if u is None:
                form['password'] = cls.salted_password(password)
                User.new(form)
                result = '注册成功'
            else:
                result = '用户名已被注册'
        else:
            result = '用户名或者密码长度必须大于2'

        return result
