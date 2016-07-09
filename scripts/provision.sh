#!/bin/sh

# Stop script execution as soon as there are any errors
set -e

pwd
now=$(date +"%T")
echo "$now Running provision.sh"

# Use the en_GB.utf8 locale
sudo update-locale LANG=en_US.utf8

# Instructions from: https://www.elastic.co/guide/en/elasticsearch/reference/1.4/setup-repositories.html
wget -qO - https://packages.elasticsearch.org/GPG-KEY-elasticsearch | sudo apt-key add -
echo 'deb http://packages.elasticsearch.org/elasticsearch/1.4/debian stable main' | sudo tee /etc/apt/sources.list.d/elasticsearch.list

# Install the packages we need
sudo apt-get update
sudo DEBIAN_FRONTEND=noninteractive apt-get dist-upgrade -y
sudo DEBIAN_FRONTEND=noninteractive apt-get install -y \
  git libffi-dev libssl-dev build-essential sqlite3 \
  python3-dev python3-pip python-virtualenv \
  openjdk-7-jre elasticsearch postgresql

# Set virtualenv directory and create it if needed.
virtualenv_dir="/home/vagrant/councilmatic-virtualenv"
[[ -d "$virtualenv_dir" ]] || virtualenv "$virtualenv_dir" --python=$(which python3)

# Install the python requirements
# We specify a long timeout and use-mirrors to avoid
# errors like "SSLError: The read operation timed out"
cd /vagrant
"$virtualenv_dir/bin/pip" install --timeout=120 --use-mirrors --requirement /vagrant/requirements.txt

# Set up the Django database
"$virtualenv_dir/bin/python" /vagrant/manage.py migrate --no-initial-data

# Set shell login message
echo "-------------------------------------------------------
Welcome to the Councilmatic vagrant machine

Run the web server with:
  ./manage.py runserver 0.0.0.0:8000

Then visit http://127.0.0.1.xip.io:8000/ to use Councilmatic

-------------------------------------------------------
" | sudo tee /etc/motd > /dev/null

# Add cd /vagrant to ~/.bashrc
grep -qG "cd /vagrant" "$HOME/.bashrc" || echo "cd /vagrant" >> "$HOME/.bashrc"

# Activate virtualenv in ~/.bashrc
grep -qG "source $virtualenv_dir/bin/activate" "$HOME/.bashrc" || echo "source $virtualenv_dir/bin/activate" >> "$HOME/.bashrc"
