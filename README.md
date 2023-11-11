
# Coursework_6
## DJANGO
### Allow to create scheduler transfer for sending messages to clients
## Requirements.
* Python
* Postgres
## Installation
* Download repo
* Install requirements (pip install -r requirements.txt)
## Prepare 
* prepare .env file (examples in .env_sample)
* create database for postgres 'mailing'
* prepare migrations (python manage.py makemigrations)
* make migrate (python manage.py migrate)
* prepare platform (python manage.py ccsu)
* python manage.py crontab add
* python manage.py runserver
## Info about users and groups
After prepare platform you will have!!!!! but (python manage.py ccsu) not working, 
I spent a lot of time, I don't know what to do. Help me please!!!
* groups moderator and users
* user lemanove@gmail.com (password 12345678)
* user moderator@gmail.com (password 12345678)
* user test@gmail.com (password 12345678)

## How it works.
* Create messages (moderators only can see, users have all rights)
* Create clients for sending (moderators only can see, users have all rights)
* Create transmissions for sending (moderators only can see and change published/unpublished status, users have all rights)
* Users can see only theirs own tasks/users/messages
* django_crontab runs schedule function every 1 minute that executes your jobs
