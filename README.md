# Social Media [![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

Social Media is a clone of Twitter, made with Django. It is still under development.

## Pre-Requisites
* Python 3+ (with pip)
* Git

## How to use
* clone the repo :  `https://github.com/PhuyalGaurav/social-media `
* Install django : `pip install django`
* If you want a new database then: 
	* Delete the previous database : `del db.sqlite3` or `rm db.sqlite3`  
	* Create a new database : `python manage.py migrate`
* Create a super user (used for admin panel) : `python manage.py runserver`
* Run the server : `python manage.py runserver`
* Visit the site at: http://127.0.0.1:8000/   
* Visit the admin panel at: http://127.0.0.1:8000/admin

## Features
* All of the posts that have been made by user is shown in the default page
* New posts can be made by a user who is logged in.
* Profile pages where you can choose to either follow or unfollow them.
* a "Following" page where there are post made only by the people you follow
* Paginations if there are more than 10 posts in a single page.
* Editing posts without refreshing the entire page (can only be done to your own posts)
* Like and unlike posts

## How to contribute  
 Just send a normal Pull request i might accept.
