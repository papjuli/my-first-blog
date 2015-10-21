# Django tutorial

I'm following the
[Django girls tutorial](http://tutorial.djangogirls.org/en/index.html)
to create a simple web application (a blog) using [Django](https://www.djangoproject.com/).

## Notes

See `notes.md`.

## Dependencies:

[Django](https://www.djangoproject.com/)

    $ pip install django

## Starting and stopping the server:

If you are starting it for the first time, you have to create a database first:

    $ python manage.py migrate

This creates an sqlite3 database.

To run the server:

    $ python manage.py runserver

Stop with Ctrl+C.

