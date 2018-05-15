import time


def log(*args, **kwargs):
    time_format = '---%Y/%m/%d %H:%M:%S---'
    local_time = time.localtime(time.time())
    formatted_time = time.strftime(time_format, local_time)

    with open('ad-web.log', 'a+', encoding='utf-8') as f:
        print(formatted_time, *args, **kwargs)
        print(formatted_time, *args, file=f, **kwargs)
