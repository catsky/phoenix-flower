phoenix-flower
==============

## introduction
A hacker news like web app built up by using Python Web Framework Flask, SQLAlchemy, Mysql/SQLite, Cron etc technologies.

## Wanna see a Demo of this project?
Yep, it's just launched on DigitalOcean. Try it via http://42bang.com

## How to deploy on my own env?
recommend to install this app on your LEMP server.

1. mysql php nginx install:
https://www.digitalocean.com/community/articles/how-to-install-linux-nginx-mysql-php-lemp-stack-on-ubuntu-12-04

2. phpmyadmin nginx
https://www.digitalocean.com/community/articles/how-to-install-phpmyadmin-on-a-lemp-server/

3. install pip
 ```
 sudo apt-get install python-pip
 ```

4. install virtualenv
```
pip install virtualenv
```

5. create the virtualenv for phoenixflower
```
virtualenv phoenixflower
```

6. active your virtual env by
```
source phoenixflower/bin/activate
```

7. install dev env in order to make the mysql dev installation smoothly
```
sudo apt-get install libmysqlclient-dev python-dev
```

8. install the requirements for this app
```
sudo apt-get install git
git clone https://github.com/catsky/phoenix-flower.git
cd phoenix-flower
pip install -r requirements.txt
```

9. rename config.back.py  to config.py, and fullfill the info according to your settings.

10. create a db called "phoenixflower" using phpmyadmin or something else

11. start this app by running
```
python index.py
```

12. access this app via 
http://localhost:5000  
ENJOY! :)

*13. OR DEPLOY ON THE PRODUCTION ENV
recommend to use nginx and uwsgi, follow the instruction below

https://www.digitalocean.com/community/articles/how-to-setup-uwsgi-on-ubuntu-12-10
https://gist.github.com/mplewis/6076082
```
 uwsgi --socket 127.0.0.1:3031 --module index  --callable app --virtualenv /root/phoenixflower/ --daemonize=/var/log/uwsgi/phoenixflower.log
```

##License
MIT
