import config
from models.user import User
from models.user_role import UserRole
from utils import log


def main():
    username = config.admin_username
    password = config.admin_password
    role = UserRole.admin

    form = dict(
        username=username,
        password=password,
        role=role,
    )

    u = User.find_by(username=username)
    if u is None:
        result = User.register(form)
    else:
        form['id'] = u.id
        result = User.update(form)

    log(result)


if __name__ == '__main__':
    main()
