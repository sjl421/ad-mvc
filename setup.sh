add-apt-repository -y ppa:deadsnakes/ppa
apt update

apt install -y python3.6 redis-server supervisor

curl https://bootstrap.pypa.io/get-pip.py > /tmp/get-pip.py
python3.6 /tmp/get-pip.py

pip3 install jinja2 redis

ln -s -f /var/www/ad-mvc/supervisor.conf /etc/supervisor/conf.d/ad-mvc.conf

service redis-server restart
service supervisor restart
