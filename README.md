Coding Samples
==============
## Python Web Developer and Dev Ops Engineer
#### Glen Baker - iepathos@gmail.com
Enthusiasm about open source, open data and open knowledge.  Self-starter comfortable working independently and in a team environment.  Self-motivated with a passion for learning new and improved techniques.

+ [Bitcoin Arbitrage](https://github.com/iepathos/arbiter) is an arbitrage program I wrote in response to a coding puzzle issued by priceonomics.com.  The program retrieves the current rates through priceonomics API and then determines the best possible arbitrage opportunity in the data set.  A directed graph of the data is created.  Arbiter uses the Bellman Ford algorithm over the negative log of the product of the edge weights along the di-graph to find negative weight cycles. Permutations of possible arbitrage cycles containing the edge with a negative weight cycle are compared and the most profitable is returned.

+ [Django and SQL Database creation](https://github.com/iepathos/codingsamples/blob/master/populate.py) I created this script for a startup website I'm working on.  This script populates a SQL database with all of the categories from the National Taxonomy of Exempt Entities and all of the non-profit organizations in the US from the IRS pub78 release.

+ [Guidestar Database Information Sync](https://github.com/iepathos/codingsamples/blob/master/guidestar.py) This script works with the database created from the previous script.  It updates the non-profit organizations in the database with information from the Guidestar database like organization mission statement, zipcode, total annual revenue and total annual expenses.  It categorizes the organizations into primary, secondary and tertiary categories and sub-categories based on Guidestar.  Additionally, if the script finds a new category on Guidestar, it will add the category to the database.

+ [Python API Assignment](https://github.com/iepathos/codingsamples/blob/master/mashup.py) is a python script I wrote in response to a coding assignment from Saffron Digital.  The script finds all of the popular music artists through Yahoo search API, then finds all of the artists' albums through LastFM API.  It finds the album name, a medium-sized image link of the album cover and the play counts for each album.  Then it spits everything out in JSON format.  One of the requirements for the challenge was that the script execute in less than 30 seconds.  My script only takes about 10 seconds to execute.

+ [Python List Comprehension](https://github.com/iepathos/codingsamples/blob/master/convertro.py) is a python script written in response to an online interview question asked by Convertro for a developer position.  The function of the script is a basic parse and sort.  The interesting part for me was the restriction to using only list comprehension to accomplish the task.

# Websites I Have Worked On
+ [GiraffL](http://www.giraffl.com/)
	I built GiraffL.com for EDN-Systems.  GiraffL is a raffling website where a lot of the proceeds are donated to charities.  I built GiraffL with Django 1.6.1 and PostgreSQL.  I used Amazon S3 with CORS for image uploads and stripe to handle credit card payments.  I optimized GiraffL to perform under high traffic.

+ [Brnable](https://www.brnable.com/)
	I built brnable.com mostly with Flask.  It's a private messaging service.  It lets you send private messages with built-in self-destruct options over any online network.  Brnable allows you to share messages with friends over Facebook without Facebook's servers ever knowing what the messages actually are. 

+ [Wyoma Films](http://glacial-castle-6814.herokuapp.com/)
	This is a portfolio site for a video production startup based in Los Angeles, CA.  I built and re-built this site multiple times, usually coinciding with new video releases for the company.  It's currently built with Django 1.5, PostgreSQL on the backend and jQuery and Bootstrap on the front.

+ [Rime Now](http://www.rimenow.com/)
	I performed dev-ops on this website, transfering it to webfactional and setting up the new server.  I had to go in and fix some old Python-Twitter API code as well in order to get the site operational.  I setup the new MySQL server and imported the information for the Django app to serve.