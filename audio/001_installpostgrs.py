sudo apt update
sudo apt upgrade -y

sudo apt install sudo

sudo apt install -y software-properties-common
sudo apt install -y postgresql-10
sudo apt install -y postgresql-client-10

sudo -u postgres psql -c "ALTER USER postgres WITH PASSWORD 'postgres';"

sudo -u postgres psql -c "CREATE EXTENSION adminpack;"

psqluser="pythonuser"   # Database username
psqlpass="pythonuser"  # Database password
psqldb="data"   # Database name

sudo printf "CREATE ROLE pythonuser WITH LOGIN SUPERUSER INHERIT CREATEDB CREATEROLE NOREPLICATION PASSWORD 'pythonuser';\nCREATE DATABASE $psqldb WITH OWNER $psqluser;" > createuserdb.sql

sudo -u postgres psql -f createuserdb.sql

sudo apt install postgis
