# es_project

## Commands used in this project

### Django

- conda activate wordcloud
  - activate conda virtual env
- django-admin startproject es_project
  - create a new Django project
- cd es_project
  - enter into (chg dir) working directory
- pip install django-cors-headers
  - add cors to header (or else BE API can't be used in FE)
- python manage.py startapp customers
  - creating a Django app
- python manage.py makemigrations (optional: app)
  - detect newly made change(s) to make migrations
- python manage.py migrate (optional: app)
  - add into tables of db
- python manage.py runserver 8080
  - run server

### PostgreSQL

- CREATE DATABASE esdb2;
  - create database
- \c esdb2
  - connect database
- \dt
  - list tables (List of relations)
- \d tweets_tweet
  - describe tables
- SELECT \* FROM django_migrations;
  - show all data in this table

Cron job command need add to crontab

- crontab -e
  open crontab in vi
  _/1 _ \* \* _ cd /Users/zrhun/Desktop/Coding/happyelementbe && /Users/zrhun/anaconda3/bin/python3 manage.py runcrons >> /Users/zrhun/Desktop/Coding/happyelementbe/tweets/log.txt 2>&1
  _/1 \* \* \* _ cd /Users/zrhun/Desktop/Coding/happyelementbe && /Users/zrhun/anaconda3/envs/wordcloud/bin/python3.10 manage.py runcrons >> /Users/zrhun/Desktop/Coding/happyelementbe/tweets/log.txt 2>&1
  _/1 \* \* \* \* cd /Users/zrhun/Desktop/Coding/happyelementbe/tweets && /Users/zrhun/anaconda3/bin/python3 testing.py >> /Users/zrhun/Desktop/Coding/happyelementbe/tweets/log.txt 2>&1

  - `*/1 * * * * cd /Users/zrhun/Desktop/Coding/happyelementbe && /Users/zrhun/anaconda3/envs/wordcloud/bin/python3.10 manage.py runcrons >> /Users/zrhun/Desktop/Coding/happyelementbe/tweets/log.txt 2>&1`

  - `*/1 * * * * cd ~/happyelementbe && source env/bin/activate && python manage.py runcrons >> tweets/log.txt 2>&1`

libs:

- pip install django_cron
  - install django_cron lib
- pip freeze > requirements.txt
  - export all libs into text file
- python3 manage.py runcrons "tweets.cron.MyCronJob"
