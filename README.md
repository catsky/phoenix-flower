phoenix-flower
==============

## introduction
a hacker news like web app built up by using Flask, SQLAlchemy etc technologies.

## Wanna see a Demo of this project?
Sorry, not now. We are working on it.

## How to deploy on my own env?
recommend to install this app on your LEMP server

1. mysql php nginx install:
https://www.digitalocean.com/community/articles/how-to-install-linux-nginx-mysql-php-lemp-stack-on-ubuntu-12-04

2. phpmyadmin nginx
https://www.digitalocean.com/community/articles/how-to-install-phpmyadmin-on-a-lemp-server/

3.  install pip
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
source bin/activate
```

7. install dev env in order to make the mysql dev installation smoothly
```
sudo apt-get install libmysqlclient-dev python-dev
```
8. install the requirements for this app
```
pip install -r requirements.txt
```

9. upload the source file of this app to your VPS

10. rename config.back.py  to config.py, and fullfill the info according to your settings.

11. create a db called "phoenixflower" using phpmyadmin or something else

12. start this app by running
```
python index.py
```

13. access this app via 
http://localhost:5000  
ENJOY! :)

##License
MIT
