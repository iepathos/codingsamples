# Coding Samples
## Web Developer and Technical Editor
### Glen Baker - iepathos@gmail.com
Enthusiasm about open source, open data and open knowledge.  Self-starter comfortable working independently and in a team environment.  Self-motivated with a passion for learning new and improved techniques.

+ [Python API coding](https://github.com/iepathos/codingsamples/blob/master/mashup.py) is a python script I wrote in response to a coding challenge from Saffron Digital.  The script finds all of the popular music artists through Yahoo search API, then finds all of the artists' albums through LastFM API.  It finds the album name, a medium-sized image link of the album cover and the play counts for each album.  Then it spits everything out in JSON format.  One of the requirements for the challenge was that the script execute in less than 30 seconds.  My script only takes about 10 seconds to execute.

+ [Django and SQL Database creation](https://github.com/iepathos/codingsamples/blob/master/populate.py) I created this script for a startup website I'm working on.  This script populates a SQL database with all of the categories from the National Taxonomy of Exempt Entities and all of the non-profit organizations in the US from the IRS pub78 release.

+ [Guidestar Database Information Sync](https://github.com/iepathos/codingsamples/blob/master/guidestar.py) This script works with the database created from the previous script.  It updates the non-profit organizations in the database with information from the Guidestar database like organization mission statement, zipcode, total annual revenue and total annual expenses.  It categorizes the organizations into primary, secondary and tertiary categories and sub-categories based on Guidestar.

+ [Python coding puzzle](https://github.com/iepathos/codingsamples/blob/master/bestbefore.py) is a python script I wrote in response to a coding puzzle from Spotify.  The script reads an ambiguous date from a file and prints the earliest possible expiration date between the years 2000 and 3000.

# Contributions to Open Source projects:
+ Fixed a couple errors by adding safety checks to [django-categories](https://github.com/callowayproject/django-categories)
+ Fixed typos in [django-progressbarupload](https://github.com/ouhouhsami/django-progressbarupload) code comments and documentation
+ Updated the Openshift actions hooks for all of the master Django project templates.  I added a pre_build action hook to simplify the projects' installation and updated the Openshift environment variables. [DIY Python2.7 Django](https://github.com/ehazlett/openshift-diy-py27-django) [DIY GeoDjango](https://github.com/bixority/openshift-diy-geodjango) [DIY Django with uWSGI and Jenkins](https://github.com/ksurya/openshift-diy-py27-django-jenkins)
+ Updated [Mezzanine CMS templates for Django](https://github.com/renyi/mezzanine-themes)
+ Fixed typos in [Django endless-pagination](https://github.com/frankban/django-endless-pagination)
+ Edited [Mark Oto's HTML and CSS Styling Guide](https://github.com/mdo/code-guide)
+ Edited [Kenneth Reitz's Python Best Practices Guide](https://github.com/kennethreitz/python-guide )
