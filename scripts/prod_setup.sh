sudo apt-get update
sudo apt-get install python-pip python3-pip git python3.4-psycopg2 libpq-dev python-dev nginx
sudo pip install virtualenv virtualenvwrapper 
sudo pip3 install virtualenv virtualenvwrapper uwsgi
echo "export VIRTUALENVWRAPPER_PYTHON=/usr/bin/python3" >> ~/.bashrc
echo "export WORKON_HOME=~/Env" >> ~/.bashrc
echo "source /usr/local/bin/virtualenvwrapper.sh" >> ~/.bashrc
source ~/.bashrc
mkvirtualenv booksonas
git clone git@github.com:phildini/bockus.git
cd bockus 
pip install -r requirements.txt
sudo mkdir -p /etc/uwsgi/sites
cd /etc/uwsgi/sites/
sudo nano booksonas.ini
sudo nano /etc/init/uwsgi.conf
sudo nano /etc/nginx/sites-available/booksonas
sudo ln -s /etc/nginx/sites-available/booksonas /etc/nginx/sites-enabled/
sudo service nginx configtest
sudo service nginx restart
sudo service uwsgi start
sudo su
echo deb http://apt.newrelic.com/debian/ newrelic non-free >> /etc/apt/sources.list.d/newrelic.list
wget -O- https://download.newrelic.com/548C16BF.gpg | apt-key add -
apt-get update
apt-get install newrelic-sysmond
nrsysmond-config --set license_key=5ab8b70f898c3c54738c176fca1cf856e375a42b
/etc/init.d/newrelic-sysmond start