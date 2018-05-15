from . import Model


class Note(Model):
    """
    用户留言
    """

    def __init__(self, form):
        super().__init__(form)
        self.title = form['title']
        self.content = form['content']
        self.user_id = int(form['user_id'])

    @classmethod
    def update(cls, form):
        note_id = int(form['id'])
        u = cls.find_by(id=note_id)

        u.title = form['title']
        u.content = form['content']
        u.save()

        return u

    def user(self):
        from .user import User
        u = User.find_by(id=self.user_id)
        return u

    def json(self):
        form = super().json()

        u = self.user()
        form['username'] = u.username

        return form
