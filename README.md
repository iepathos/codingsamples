Coding Samples
==============
## Coder and Technical Editor
#### Glen Baker - iepathos@gmail.com
Enthusiasm about open source, open data and open knowledge.  Self-starter comfortable working independently and in a team environment.  Self-motivated with a passion for learning new and improved techniques.

+ [Bitcoin Arbitrage](https://github.com/iepathos/arbiter) is an arbitrage program I wrote in response to a coding puzzle issued by priceonomics.com.  The program retrieves the current rates through priceonomics API and then determines the best possible arbitrage opportunity in the data set.  A directed graph of the data is created.  Arbiter uses the Bellman Ford algorithm over the negative log of the product of the edge weights along the di-graph to find negative weight cycles. Permutations of possible arbitrage cycles containing the edge with a negative weight cycle are compared and the most profitable is returned.

+ [Python API Coding Puzzle](https://github.com/iepathos/codingsamples/blob/master/mashup.py) is a python script I wrote in response to a coding challenge from Saffron Digital.  The script finds all of the popular music artists through Yahoo search API, then finds all of the artists' albums through LastFM API.  It finds the album name, a medium-sized image link of the album cover and the play counts for each album.  Then it spits everything out in JSON format.  One of the requirements for the challenge was that the script execute in less than 30 seconds.  My script only takes about 10 seconds to execute.

+ [Django Jewelry App](https://whois-iepathos.rhcloud.com/jewelry) written in response to Beachmint backend coding exam. [Models](https://github.com/iepathos/beachmint/blob/master/jewelry/models.py) [Views](https://github.com/iepathos/beachmint/blob/master/jewelry/views.py) [Templates](https://github.com/iepathos/beachmint/tree/master/templates/jewelry)

+ [Django and SQL Database creation](https://github.com/iepathos/codingsamples/blob/master/populate.py) I created this script for a startup website I'm working on.  This script populates a SQL database with all of the categories from the National Taxonomy of Exempt Entities and all of the non-profit organizations in the US from the IRS pub78 release.

+ [Guidestar Database Information Sync](https://github.com/iepathos/codingsamples/blob/master/guidestar.py) This script works with the database created from the previous script.  It updates the non-profit organizations in the database with information from the Guidestar database like organization mission statement, zipcode, total annual revenue and total annual expenses.  It categorizes the organizations into primary, secondary and tertiary categories and sub-categories based on Guidestar.  Additionally, if the script finds a new category on Guidestar, it will add the category to the database.

+ [Python List Comprehension](https://github.com/iepathos/codingsamples/blob/master/convertro.py) is a python script written in response to an online interview question asked by Convertro for a developer position.  The function of the script is a basic parse and sort.  The interesting part for me was the restriction to using only list comprehension to accomplish the task.

# Contributions to Open Source projects:
+ Added javascript to auto-focus on form fields [pinax/pinax-theme-bootstrap](https://github.com/pinax/pinax-theme-bootstrap)
+ Edited readme for [plupload](https://github.com/moxiecode/plupload)
+ Created [django-mysql-example](https://github.com/iepathos/django-mysql-example) template for quickstart deployment of Django with MySQL on OpenShift.
+ Created [django-memcached-openshift](https://github.com/iepathos/django-memcached-openshift) template for quickstart deployment of Django with Memcached on OpenShift.
+ Added production environment safety check to the official [OpenShift Django quickstart template](https://github.com/openshift/django-example).  Fixed internal server error caused by the setup script installing the wrong version of Django.
+ Fixed a couple errors by adding safety checks to [django-categories](https://github.com/callowayproject/django-categories)
+ Fixed typos in [django-progressbarupload](https://github.com/ouhouhsami/django-progressbarupload) code comments and documentation
+ Updated the Openshift actions hooks for all of the master Django project templates.  I added a pre_build action hook to simplify the projects' installation and updated the Openshift environment variables. [DIY Python2.7 Django](https://github.com/ehazlett/openshift-diy-py27-django) [DIY GeoDjango](https://github.com/bixority/openshift-diy-geodjango) [DIY Django with uWSGI and Jenkins](https://github.com/ksurya/openshift-diy-py27-django-jenkins)
+ Updated [Mezzanine CMS templates for Django](https://github.com/renyi/mezzanine-themes)
+ Fixed typos in [Django endless-pagination](https://github.com/frankban/django-endless-pagination)
+ Edited [Mark Oto's HTML and CSS Styling Guide](https://github.com/mdo/code-guide)
+ Edited [Kenneth Reitz's Python Best Practices Guide](https://github.com/kennethreitz/python-guide )
