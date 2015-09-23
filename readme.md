# Django tutorial

I'm following the
[Django girls tutorial](http://tutorial.djangogirls.org/en/index.html)
to create a simple web application (a blog) using [Django](https://www.djangoproject.com/).

## Notes

### Creating the skeleton

To create some scripts and settings files in this dir.

    $ pyenv virtualenv 2.7.9 django
    $ pyenv activate django
    $ pip install django
    $ cd tutorials/djangogirls
    $ django-admin startproject mysite .

And also:

- change TIME_ZONE in `settings.py`
- add `STATIC_ROOT = os.path.join(BASE_DIR, 'static')` at the end of `settings.py`


To create an sqlite3 database (this is set in `settings.py` ny default):

    $ python manage.py migrate

To run the server:

    $ python manage.py runserver

Create an application called 'blog':

    $ python manage.py startapp blog

* Add `'blog'` to `INSTALLED_APPS` in `mysite/settings.py`


### Creating a model

Add a model to `blog/models.py`:

    from django.db import models
    from django.utils import timezone
     
    class Post(models.Model):
      author = models.ForeignKey('auth.User')
      title = models.CharField(max_length=200)
      text = models.TextField()
      created_date = models.DateTimeField(default=timezone.now)
      published_date = models.DateTimeField(blank=True, null=True)
      
      def publish(self):
        self.published_date = timezone.now()
        self.save()
      
      def __str__(self):
        return self.title

* `models.Model` means that the Post is a Django Model, so Django knows that it should be saved in the database.
* `models.ForeignKey` - this is a link to another model.


### Creating tables for models in the database

To tell django about the new model:

    python manage.py makemigrations blog

Django prepared for us a migration file `blog/migrations/0001_initial.py` that we have to apply now to our database:

    python manage.py migrate blog


### Django admin

To add, edit and delete posts we've just modeled, we will use Django admin. Register the Post model by replacing `blog/admin.py` by:

    from django.contrib import admin
    from .models import Post
    
    admin.site.register(Post)

We can use Django admin through the browsert at `http://127.0.0.1:8000/admin/`, but first we need to create a superuser (it will prompt for username, email address and password (régi szá.)):

    python manage.py createsuperuser

After this, we can sign in to the admin page above and create a post there for example. See the [django admin docs](https://docs.djangoproject.com/en/1.8/ref/contrib/admin/).


### Deployment





