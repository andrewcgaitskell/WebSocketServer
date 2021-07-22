# install nginx

sudo apt install nginx

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

# add external ip address to DNS record


# make index.html


    cd /var/www
    sudo mkdir listener
    cd listener
    sudo nano index.html

# paste html into file

    <!doctype html>
    <html>
    <head>
        <meta charset="utf-8">
        <title>Hello, Listener!</title>
    </head>
    <body>
        <h1>Hello, Player!</h1>
        <p>Debian!</p>
    </body>
    </html>

# change to correct site folder

cd /etc/nginx/sites-enabled

# create site file

sudo nano listener

# paste following into file

       server {
              listen 81;
              listen [::]:81;

              server_name acgtest.info;

              root /var/www/listener;
              index index.html;

              location / {
                      try_files $uri $uri/ =404;
              }
              location /game {
                 include proxy_params;
                 proxy_set_header X-Real-IP  $remote_addr;
                 proxy_set_header X-Forwarded-For $remote_addr;
                 proxy_set_header Host $host;
                 proxy_headers_hash_max_size 1024;
                 proxy_headers_hash_bucket_size 256;
                 proxy_pass http://127.0.0.1:5000/;
              }
              location /api1 {
                 include proxy_params;
                 proxy_set_header X-Real-IP  $remote_addr;
                 proxy_set_header X-Forwarded-For $remote_addr;
                 proxy_set_header Host $host;
                 proxy_headers_hash_max_size 1024;
                 proxy_headers_hash_bucket_size 256;
                 proxy_pass http://127.0.0.1:5001/;
               }
              location /socket.io/ {
                 include proxy_params;
                 proxy_http_version 1.1;
                 proxy_buffering off;
                 proxy_set_header Upgrade $http_upgrade;
                 proxy_set_header Connection "Upgrade";
                 proxy_pass http://127.0.0.1:5006/socket.io/;
               }
               location /sock {
                 include proxy_params;
                 proxy_http_version 1.1;
                 proxy_buffering off;
                 proxy_set_header Upgrade $http_upgrade;
                 proxy_set_header Connection "Upgrade";
                 proxy_pass http://127.0.0.1:5006;
               }
               location /hello {
                     uwsgi_pass 127.0.0.1:5010;
                     include uwsgi_params;
                     }

       }

ctrl x to exit and agree to save

# activate site

service nginx restart

# open ports

       81 on gcp portal
       5000
       5001

# wait a few mins

# visit site

acgtest.com:81

