import time

from . import Model


class Session(Model):
    """
    用于关联用户和会话
    """
    def __init__(self, form):
        super().__init__(form)
        self.session_id = form['session_id']
        self.user_id = form['user_id']
        self.expired_time = form.get('expired_time', time.time() + 3600)

    def expired(self):
        now = time.time()
        result = self.expired_time < now
        return result
