PROJECT_NAME='socketio1'
FRAMEWORK='gunicorn'

sudo systemctl stop $PROJECT_NAME
sudo systemctl disable $PROJECT_NAME

sudo cp /home/andrew_gaitskell/Games/TicTacToe-Pygame/$FRAMEWORK/$PROJECT_NAME/$PROJECT_NAME.service.txt /etc/systemd/system/$PROJECT_NAME.service

sudo systemctl daemon-reload

sudo systemctl start $PROJECT_NAME
sudo systemctl enable $PROJECT_NAME

sudo systemctl status $PROJECT_NAME

sudo nginx -t

sudo systemctl restart nginx

sudo systemctl status nginx
