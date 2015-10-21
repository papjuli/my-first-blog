These are the notes of the 
[Django girls tutorial](http://tutorial.djangogirls.org/en/index.html)
to create a simple web application (a blog) using [Django](https://www.djangoproject.com/).


# Creating the skeleton

### To make a pyenv virtualenv and install django:

    $ pyenv virtualenv 2.7.9 django
    $ pyenv activate django
    $ pip install django

### To start a django project:

    $ cd tutorials/djangogirls
    $ django-admin startproject mysite .
    
This creates some scripts and settings files in the `mysite` directory.
Then:

- change TIME_ZONE in `settings.py`
- add `STATIC_ROOT = os.path.join(BASE_DIR, 'static')` at the end of `settings.py`


### To create an sqlite3 database (this is set in `settings.py` by default):

    $ python manage.py migrate

### To run the server:

    $ python manage.py runserver

### Create an application called 'blog':

    $ python manage.py startapp blog

* Add `'blog'` to `INSTALLED_APPS` in `mysite/settings.py`


# Creating a model

A model is the single, definitive source of data about your data. It contains the essential fields and behaviors of the data you’re storing. Generally, each model maps to a single database table.

### Add a model to `blog/models.py`:

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


# Creating tables for models in the database

To tell django about the new model:

    python manage.py makemigrations blog

Django prepared for us a migration file `blog/migrations/0001_initial.py` that we have to apply now to our database:

    python manage.py migrate blog


# Django admin

To add, edit and delete posts we've just modeled, we will use Django admin. **Register the Post model** by replacing the contents of the file `blog/admin.py` by:

    from django.contrib import admin
    from .models import Post
    
    admin.site.register(Post)

We can use Django admin through the browser at `http://127.0.0.1:8000/admin/`, but first we need to create a superuser (it will prompt for username, email address and password (régi sz.á.)):

    python manage.py createsuperuser

After this, we can sign in to the admin page above and create a post there for example. See the [django admin docs](https://docs.djangoproject.com/en/1.8/ref/contrib/admin/).


# Deployment

## Publishing as a git repo: 

In the `djangogirls` directory

    git init

Make a `djangogirls/.gitignore` file with:

    *.pyc
    __pycache__
    myvenv
    db.sqlite3
    /static
    .DS_Store

Then commit.

On github, create a repository named `my-first-blog`, and hook them up:

    git remote add origin https://github.com/<your-github-username>/my-first-blog.git
    git push -u origin master

## Publish the website on PythonAnywhere

Sign up to [PythonAnywhere](www.pythonanywhere.com), then `yourusername.pythonanywhere.com` will be yours.

Then open a bash console on PythonAnywhere and clone the git repo:
    git clone https://github.com/<your-github-username>/my-first-blog.git

### Create a virtualenv on PythonAnywhere:

    $ cd my-first-blog
    $ virtualenv --python=python3.4 myvenv
    $ source myvenv/bin/activate
    (mvenv) $  pip install django whitenoise

### Collecting static files:

Static files are the files that don't regularly change or don't run programming code, such as HTML or CSS files. They work differently on servers compared to on our own computer and we need a tool like "whitenoise" to serve them.

    (mvenv) $ python manage.py collectstatic

### Creating the database on PythonAnywhere:

Here's another thing that's different between your own computer and the server: it uses a different database. So the user accounts and posts can be different on the server and on your computer. We can initialise the database on the server just like we did the one on your own computer, with migrate and createsuperuser:

    (mvenv) $ python manage.py migrate
    (mvenv) $ python manage.py createsuperuser

### Publishing our blog as a web app:

Click back to the PythonAnywhere dashboard by clicking on its logo, and go click on the Web tab. Finally, hit Add a new web app.
After confirming your domain name, choose manual configuration (NB not the "Django" option) in the dialog. Next choose Python 3.4, and click Next to finish the wizard.

You'll be taken to the PythonAnywhere config screen for your webapp, which is where you'll need to go whenever you want to make changes to the app on the server.
In the "Virtualenv" section, click the red text that says "Enter the path to a virtualenv", and enter: /home/<your-username>/my-first-blog/myvenv/. Click the blue box with the check mark to save the path before moving on.

### Configuring the WSGI file:

Django works using the "WSGI protocol", a standard for serving websites using Python, which PythonAnywhere supports. The way we configure PythonAnywhere to recognise our Django blog is by editing a WSGI configuration file.

Click on the "WSGI configuration file" link (in the "Code" section near the top of the page -- it'll be named something like /var/www/<your-username>_pythonanywhere_com_wsgi.py), and you'll be taken to an editor.

Delete all the contents and replace them with something like this:

    import os
    import sys
    
    path = '/home/<your-username>/my-first-blog'  # use your own username here
    if path not in sys.path:
      sys.path.append(path)
    
    os.environ['DJANGO_SETTINGS_MODULE'] = 'mysite.settings'
    
    from django.core.wsgi import get_wsgi_application
    from whitenoise.django import DjangoWhiteNoise
    application = DjangoWhiteNoise(get_wsgi_application())

Hit Save and then go back to the Web tab.
We're all done! Hit the big green Reload button and you'll be able to go view your application. You'll find a link to it at the top of the page.

You are live!

The default page for your site should say "Welcome to Django", just like it does on your local computer. Try adding /admin/ to the end of the URL, and you'll be taken to the admin site. Log in with the username and password, and you'll see you can add new Posts on the server.


# Django urls

In the `mysite/urls.py` file, Django already added the urls for the admin sites by

    url(r'^admin/', include(admin.site.urls)),

It means that for every URL that starts with `admin/` Django will find a corresponding view.

Django uses regex to match urls. Some useful regex patterns:

- `^` for beginning of the text
- `$` for end of text
- `\d` for a digit
- `+` to indicate that the previous item should be repeated at least once
- `()` to capture part of the pattern

For example the url `http://www.mysite.com/post/12345/` would match the regex `^post/(\d+)/$` (since the beginning of the url is cut off before...).

Add the line 
    url(r'', include('blog.urls')),
*after* the admin line to `mysite/urls.py`, and the urls not beginning with admin will be redirected to `blog/urls.py` and resolved there. In `blog/urls.py` we put:

    from django.conf.urls import url
    from . import views
    
    urlpatterns = [
      url(r'^$', views.post_list, name='post_list'),
      url(r'^post/(?P<pk>[0-9]+)/$', views.post_detail, name='post_detail'),
    ]

This assigns the view called post_list to the (empty ending) `^$` url and the view called post_detail to a url like `http://www.mysite.com/post/12345/`.


# Django views

Views, like `views.post_list` and `views.post_detail` are functions (defined in `views.py`) that are called when a request comes, with the request as the first parameter and in the case of `views.post_detail`, the part `?P<pk>` in the URL configuration has the result that the post number is also given to the view as a parameter named `pk` (pk stands for primary key).


# HTML templates

Templates are used to generate HTMLs dynamically. A template contains the static parts of the desired HTML output as well as some special syntax describing how dynamic content will be inserted. We'll look at the syntax later in the "Django templates" section.

We put our html templates in the `blog/templates/blog` directory. 


# Django QuerySets

Once you’ve created your data models, Django automatically gives you a database-abstraction API that lets you create, retrieve, update and delete objects. You can try it out in the Django interactive shell:

    $ python manage.py shell

First import the Post and User models:

    >>> from blog.models import Post
    >>> from django.contrib.auth.models import User

### Some basic queries:

 - `>>> Post.objects.all()` lists all the posts in the database
 - `>>> me = User.objects.get(username='papjuli')` gets a user
 - `>>> Post.objects.create(author=me, title='Sample title', text='Test')` creates a new post

We can call a function of a model:

    >>> post = Post.objects.get(title="Sample title")
    >>> post.publish()
    
publishes the post.

### Filter queries

    >>> Post.objects.filter(author=me)
gets the posts of the user stored in `me`.

    >>> Post.objects.filter(title__contains='title')
gets all the posts that contain a word 'title' in the title field.

    >>> from django.utils import timezone
    >>> Post.objects.filter(published_date__lte=timezone.now())
gets the posts that have published_date set in the past.

### Ordering

`>>> Post.objects.order_by('created_date')`

gets all the posts ordered by the `created_date` field.

`>>> Post.objects.order_by('-created_date')`

`-` for reverse order.

### Chaining queries:

`>>> Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')`

### Closing the interactive shell

`>>> exit()`


# Dynamic data in templates

In the views we want to "fill out" some templates we want, with the data corresponding to some models. Dhango's "render" function can do this for us (see `blog/views.py`):

    def post_list(request):
      posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')
      return render(request, 'blog/post_list.html', {'posts': posts})

In this view, we first get the published posts sorted by `published_date` and handed them to the render function as a variable called `posts`, and also the `blog/post_list.html` template to fill in with the date, title and text of the post. That template in turn imports the `blog/base.html` template in the beginning. (The paths of the template files are relative to the directory `./blog/templates`.)


# Django templates

To refer to some data and manipulate it in the html templates, django has built-in template language called *Django template language*. The shortest use (in `blog/templates/blog/post_list.html`) would be like this:

    {{ posts }}

which would put something like this in the html:

    [<Post: My second post>, <Post: My first post>]

A for loop looks like this:

    {% for post in posts %}
      {{ post }}
    {% endfor %}

We can access attributes and we can mix HTML and template tags:

    {% for post in posts %}
      <div>
        <p>published: {{ post.published_date }}</p>
        <h1><a href="">{{ post.title }}</a></h1>
        <p>{{ post.text|linebreaks }}</p>
      </div>
    {% endfor %}

The `{{ post.text|linebreaks }}` part means that the text is piped into a *filter*, which converts line-breaks into paragraphs. Some filters take an argument:

    {{ my_date|date:"Y-m-d" }}

The line 

    <h1><a href="{% url 'post_detail' pk=post.pk %}">{{ post.title }}</a></h1>

in `post_list.html` means that django makes a url from the pattern named 'post_detail' with the value of `post.pk` as argument `pk`.

See [here](https://docs.djangoproject.com/en/1.8/topics/templates/#the-django-template-language) for more about the django template language syntax and [here](https://docs.djangoproject.com/en/1.8/ref/templates/builtins/#ref-templates-builtins-filters) for a reference of built-in filters.

An interesting thing: if a variable (in {{ }}) resolves to a callable, the template system will call it with no arguments and use its result instead of the callable. I tried this out with a number generator: it counts the number of html requests for both the blog page and the separate post pages together (from the last time the django server was started or updated its imports).

## Template extending

An html template can include another template, this way we don't have to repeat ourselves in every file, if we want a part to be the same, like the head of the page. For example the line 

    {% extends "blog/base.html" %}

includes `blog/base.html` in `blog/post_list.html` in the way that the block defined in `post_list.html` goes where `{% block content %}` is in the `base.html`


# CSS

For css, we use [Bootstrap](http://getbootstrap.com/) as a base. It is included in the  `blog/templates/blog/base.html` template.

Our own css files should go in the `blog/static` directory: the django template tag `{% load staticfiles %}` in `base.html` loads them automatically (or actually from any folder called static inside the folder of the app). A certain css file is then included in the html like this (in the head, after the links to the bootstrap css files):

    <link rel="stylesheet" href="{% static 'css/blog.css' %}">





