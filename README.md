# ad-mvc

基于 Socket 和 HTTP 的 Web MVC 框架。

## 结构

| 文件/目录  |   说明   |    分层    |
| ---------- | -------- | ---------- |
| server.py  | 程序入口 | -          |
| models/    | 数据模型 | Model      |
| routes/    | 转发路由 | Controller |
| templates/ | 前端模板 | View       |
| static/    | 静态资源 | -          |

## 部署

### 部署代码

```bash
mkdir -p /var/www
cd /var/www
git cloue https://github.com/accelad/ad-mvc.git
```

### 配置敏感数据

进入`ad-mvc`目录下，新建`config.py`文件。

```bash
cd /var/www/ad-mvc
touch confg.py
```

编辑`config.py`文件，增加如下属性并自定义值：

```python
redis_prefix = 'xxxxx'
```

`redis_prefix`可用于区分不同项目。

### 执行部署脚本

```bash
cd /var/www/ad-mvc
bash -ex setup.sh
```

### 修改`server`的监听`ip`和`port`（可选）

编辑`supervisor.conf`文件，修改`command`属性中的`host`和`port`参数值：

```conf
command=/usr/bin/python3 server.py --host localhost --port 8000
```

修改完毕后，再次执行部署脚本即可生效。

### 设置管理员账户（可选）

编辑`config.py`文件，增加如下属性并自定义值：

```python
admin_username = 'xxxxx'
admin_password = 'xxxxx'
```

执行`reset.py`，即可将该账户设置为管理员。

```bash
cd /var/www/ad-mvc
python3 reset.py
```

## 链接

[https://mvc.accelad.xyz](https://mvc.accelad.xyz)
