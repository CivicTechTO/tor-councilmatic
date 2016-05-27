apt-get update
apt-get upgrade --yes
apt-get install --yes openjdk-7-jre git-core python3 python3-pip postgresql-9.3 postgresql-server-dev-9.3
wget --continue https://download.elastic.co/elasticsearch/elasticsearch/elasticsearch-1.7.2.deb
dpkg -i elasticsearch-1.7.2.deb
update-rc.d elasticsearch defaults

BASHRC=/home/vagrant/.bashrc
grep python3 $BASHRC > /dev/null || echo alias python=/usr/bin/python3 >> $BASHRC

cd /vagrant
export PIP=pip3
make pip-install
export DATABASE_URL=postgres:///tor_councilmatic
sudo --preserve-env --user postgres createdb tor_councilmatic
sudo --preserve-env --user postgres python3 manage.py migrate --no-initial-data
sudo --preserve-env --user postgres python3 manage.py runserver 9501
