# install nginx

sudo su

apt install nginx

# check server

systemctl status nginx

## if you get an error

mkdir /etc/systemd/system/nginx.service.d

printf "[Service]\nExecStartPost=/bin/sleep 0.1\n" > /etc/systemd/system/nginx.service.d/override.conf

## reload and start

systemctl daemon-reload

systemctl restart nginx

# check status

systemctl status nginx
