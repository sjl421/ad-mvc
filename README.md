# ad-mvc
基于 Socket 和 HTTP 的 Web MVC 框架。

## 结构
| 文件/目录  |   说明    |    分层    |
| ---------- | --------- | ---------- |
| server.py  | 程序入口  | -          |
| models/    | 数据模型  | Model      |
| routes/    | 转发路由  | Controller |
| templates/ | HTML 模板 | View       |
| static/    | 静态资源  | -          |

## 部署
### 部署代码
```bash
mkdir -p /var/www
cd /var/www
git cloue https://github.com/accelad/ad-mvc.git
```

### 执行部署脚本
```bash
cd /var/www/ad-mvc
bash -ex setup.sh
```

### 设置管理员账户（可选）
在`ad-mvc`目录下，新建一个`config.py`，可用于注册管理员账户，格式如下：

```python
admin_username = 'xxxxx'
admin_password = 'xxxxx'
```

执行`reset.py`，即可将配置的账户注册为管理员。

```bash
cd /var/www/ad-mvc
python3 reset.py
```

## 样例
[https://mvc.accelad.xyz](https://mvc.accelad.xyz)
