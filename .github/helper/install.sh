#!/bin/bash

set -e

cd ~ || exit

pip install frappe-bench

bench init frappe-bench --skip-assets --python "$(which python)" --frappe-path "${GITHUB_WORKSPACE}"

mkdir ~/frappe-bench/sites/test_site
cp ${GITHUB_WORKSPACE}/.travis/mariadb.json ~/frappe-bench/sites/test_site/site_config.json


mysql --host 127.0.0.1 --port 3306 -u root -e "SET GLOBAL character_set_server = 'utf8mb4'";
mysql --host 127.0.0.1 --port 3306 -u root -e "SET GLOBAL collation_server = 'utf8mb4_unicode_ci'";

mysql --host 127.0.0.1 --port 3306 -u root -e "CREATE DATABASE test_frappe_consumer";
mysql --host 127.0.0.1 --port 3306 -u root -e "CREATE USER 'test_frappe_consumer'@'localhost' IDENTIFIED BY 'test_frappe_consumer'";
mysql --host 127.0.0.1 --port 3306 -u root -e "GRANT ALL PRIVILEGES ON \`test_frappe_consumer\`.* TO 'test_frappe_consumer'@'localhost'";

mysql --host 127.0.0.1 --port 3306 -u root -e "CREATE DATABASE test_frappe_producer";
mysql --host 127.0.0.1 --port 3306 -u root -e "CREATE USER 'test_frappe_producer'@'localhost' IDENTIFIED BY 'test_frappe_producer'";
mysql --host 127.0.0.1 --port 3306 -u root -e "GRANT ALL PRIVILEGES ON \`test_frappe_producer\`.* TO 'test_frappe_producer'@'localhost'";

mysql --host 127.0.0.1 --port 3306 -u root -e "UPDATE mysql.user SET Password=PASSWORD('travis') WHERE User='root'";
mysql --host 127.0.0.1 --port 3306 -u root -e "FLUSH PRIVILEGES";

cd ./frappe-bench || exit

sed -i 's/^watch:/# watch:/g' Procfile
sed -i 's/^schedule:/# schedule:/g' Procfile

sed -i 's/^socketio:/# socketio:/g' Procfile
sed -i 's/^redis_socketio:/# redis_socketio:/g' Procfile

cd ./apps/frappe || exit
yarn add node-sass@4.13.1
cd ../..

bench start &
bench --site test_site reinstall --yes

bench build --app frappe