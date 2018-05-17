import os

from jinja2 import (
    Environment,
    FileSystemLoader,
)


def initialized_environment():
    path = os.path.join(os.path.dirname(__file__), 'templates')
    # 创建一个加载器, jinja2 会从这个目录中加载模板
    loader = FileSystemLoader(path)
    # 用加载器创建一个环境, 有了它才能读取模板文件
    # 启用自动转义，以防 xss
    e = Environment(
        autoescape=True,
        loader=loader,
    )
    return e


class Template:
    e = initialized_environment()

    @classmethod
    def render(cls, filename, *args, **kwargs):
        # 调用 get_template() 方法加载模板并返回
        template = cls.e.get_template(filename)
        # 用 render() 方法渲染模板
        # 可以传递参数
        return template.render(*args, **kwargs)
