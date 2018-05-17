apt update
apt install -y python3 python3-pip supervisor
pip3 install jinja2

ln -s -f /var/www/ad-mvc/supervisor.conf /etc/supervisor/conf.d/ad-mvc.conf

service supervisor restart
