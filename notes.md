These are the notes of the 
[Django girls tutorial](http://tutorial.djangogirls.org/en/index.html)
to create a simple web application (a blog) using [Django](https://www.djangoproject.com/).


# Creating the skeleton

### To make a pyenv virtualenv and install django:

    $ pyenv virtualenv 2.7.9 django
    $ pyenv activate django
    $ pip install django

To start a django project:

    $ cd tutorials/djangogirls
    $ django-admin startproject mysite .
    
This creates some scripts and settings files in the `mysite` directory.
Then:

- change TIME_ZONE in `settings.py`
- add `STATIC_ROOT = os.path.join(BASE_DIR, 'static')` at the end of `settings.py`


To create an sqlite3 database (this is set in `settings.py` by default):

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

To add, edit and delete posts we've just modeled, we will use Django admin. Register the Post model by replacing the contents of the file `blog/admin.py` by:

    from django.contrib import admin
    from .models import Post
    
    admin.site.register(Post)

We can use Django admin through the browser at `http://127.0.0.1:8000/admin/`, but first we need to create a superuser (it will prompt for username, email address and password (régi sz.á.)):

    python manage.py createsuperuser

After this, we can sign in to the admin page above and create a post there for example. See the [django admin docs](https://docs.djangoproject.com/en/1.8/ref/contrib/admin/).


### Deployment

#### Publishing as a git repo: 

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

#### Publish the website on PythonAnywhere

Sign up to [PythonAnywhere](www.pythonanywhere.com), then `yourusername.pythonanywhere.com` will be yours.

Then open a bash console on PythonAnywhere and clone the git repo:
    git clone https://github.com/<your-github-username>/my-first-blog.git

Create a virtualenv on PythonAnywhere:

    $ cd my-first-blog
    $ virtualenv --python=python3.4 myvenv
    $ source myvenv/bin/activate
    (mvenv) $  pip install django whitenoise

Collecting static files:

Static files are the files that don't regularly change or don't run programming code, such as HTML or CSS files. They work differently on servers compared to on our own computer and we need a tool like "whitenoise" to serve them.

    (mvenv) $ python manage.py collectstatic

Creating the database on PythonAnywhere:

Here's another thing that's different between your own computer and the server: it uses a different database. So the user accounts and posts can be different on the server and on your computer. We can initialise the database on the server just like we did the one on your own computer, with migrate and createsuperuser:

    (mvenv) $ python manage.py migrate
    (mvenv) $ python manage.py createsuperuser

Publishing our blog as a web app:

Click back to the PythonAnywhere dashboard by clicking on its logo, and go click on the Web tab. Finally, hit Add a new web app.
After confirming your domain name, choose manual configuration (NB not the "Django" option) in the dialog. Next choose Python 3.4, and click Next to finish the wizard.

You'll be taken to the PythonAnywhere config screen for your webapp, which is where you'll need to go whenever you want to make changes to the app on the server.
In the "Virtualenv" section, click the red text that says "Enter the path to a virtualenv", and enter: /home/<your-username>/my-first-blog/myvenv/. Click the blue box with the check mark to save the path before moving on.

Configuring the WSGI file:

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



