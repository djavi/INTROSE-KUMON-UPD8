@echo off

title Server Console
echo Starting server.....

cd desktop
cd INTROSE
cd KumonSite

start "" http://localhost:8000/kumon/login/

python manage.py runserver 0.0.0.0:8000

