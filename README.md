# mloss.org

This is the source code of the [mloss.org](http://mloss.org) website. It was written by the
mloss team, which currently is (in alphabetical order)

[Mikio Braun](mikio@cs.tu-berlin.de)
[Cheng Soon Ong](mailto:chengsoon.ong@inf.ethz.ch)
[Soeren Sonnenburg](mailto:soeren.sonnenburg@first.fraunhofer.de)


##Features

The website contains quite a few features and is also quite specific,
so you may or may not find it useful for your means. The features include:

* a registration system for users of the site
* a database of user submitted software projects
* a rating system for the projects
* a commenting system for the projects
* access-statistics to the projects
* a blog (although articles have to be entered directly through django's
  admin interface)
* a forum
* email notifications for tracking projects and the forum
* a tool which automatically extracts projects in the "machine learning"
  section from CRAN (a repository for packages for the R programming 
  language)

The source code is organized into several sub-directories, so called
"applications". Each directory is organized more or less according to
the django standard, at least containing a definition of the models in
models.py, and of the url mappings in `urls.py`. If you want to find out
how a specific url is processed, have a look at the `urls.py` which tell
you which method takes care of the request.

##Changelog

###June 2013

  * Moving to Django 1.5.1:
   - Remove verify_exists from URLField (deprecated in Django 1.5)
   - Replace from django.utils.hashcompat import sha_constructor with hashlib.sha1
   - Update settings.py to set DATABASES
   - Removed django.middleware.csrf.CsrfResponseMiddleware
   - Updated django.conf.urls
   - Replace django.views.generic.list_detail.object_list with django.views.generic.list.ListView
   - Replace django.views.generic.simple.direct_to_template with django.views.generic.base.TemplateView
   - Update django.contrib.syndication.feed
   - Replace django.views.generic.list_detail.object_detail with django.views.generic.detail.DetailView

   - Added {% csrf_token %} to templates
   - Replace django.views.generic.date_based with django.views.generic.dates
   - Use django.core.paginator

  * Needed to install
   - recaptcha-client-1.0.6
   - Markdown-2.3.1


###mloss.org svn-r482-September-2008

  * Several bugfixes and adjustments related to last minute
    changes in django 1.0:

   - comments now don't require a password
   - search didn't work when returning >10 results
   - added #of subscriptions to list view
   - better interlinking between forum and blog
   - fix comments links in blog and show archive,
   - option to filter by published in JMLR
   - minor style changes
   - change sorting order in forum (new threads first)

###mloss.org svn-r470-August-2008

 * Initial Release


##License

The source code is licensed under GPLv3, and incorporates the work of
a number of projects, cf. LICENSE for details.


##Installing

You can get the mloss website development server set up as follows:

* Make sure you have virtualenv installed: `pip install virtualenv`.
* Clone the mloss website sources: `git clone TODO`.
* Run `virtualenv mloss` to setup virtualenv for the mloss code repository.
* Install all the required packages:

    cd mloss
    pip install -r requirements.txt

* The development system should now be ready. In each console that you want call
  some of the mloss python code first initialize the environment:

    source bin/activate

* Captcha TODO

* Finally, to setup the database and run the
  webserver you need to call the following two commands:

    python manage.py syncdb
    python manage.py runserver

* Open http://127.0.0.1:8000 in a web browser.
