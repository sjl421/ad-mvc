apt update
apt install -y python3 python3-pip redis supervisor
pip3 install jinja2 redis

ln -s -f /var/www/ad-mvc/supervisor.conf /etc/supervisor/conf.d/ad-mvc.conf

service redis-server restart
service supervisor restart
