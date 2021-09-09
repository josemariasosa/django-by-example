# django-by-example
Backup of the examples from the book: Django 3 by Example - Antonio Melé

## Commands

```sh
django-admin startproject bookmarks
django-admin startapp account
python manage.py startapp blog
python manage.py createsuperuser
python manage.py runserver
```

## Using the shell interface

```sh
python manage.py shell
```

```py
from django.contrib.auth.models import User
from blog.models import Post
user = User.objects.get(username='jomsox')
```

## Postgres

```sh
sudo su - postgres
createuser -dP blog
```

To create a db, you must fist change the `pg_hba.conf` file:

```sh
sudo vim /etc/postgresql/12/main/pg_hba.conf

## "local" is for Unix domain socket connections only
#local   all             all                                     md5
## IPv4 local connections:
#host    all             all             127.0.0.1/32            md5
## IPv6 local connections:
#host    all             all             ::1/128                 md5
```

Set them all from `peer` to `md5`. And then restart `postgres`:

```sh
sudo service postgresql restart
```

### Using the search feature in Postgres

Simple search:

```py
from blog.models import Post
Post.objects.filter(body__search='django')
```

Using a Search Vector, to search in multiple fields:

```py
from django.contrib.postgres.search import SearchVector
from blog.models import Post
Post.objects.annotate(search=SearchVector('title', 'body')).filter(search='sun')
```

