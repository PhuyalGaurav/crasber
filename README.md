# CrasBer [![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

#### [Video Demo](https://www.youtube.com/watch?v=pUYkWfYBmys)
CrasBer is just another take at a social media app, made with Django. It is still under development.

## Pre-Requisites
* Python 3+ (with pip)
* Git

## How its made
### I am excited to share details about my recent project, a dynamic web application developed using Django, a high-level Python web framework that encourages rapid development and clean, pragmatic design. This project showcases my ability to leverage various technologies and programming languages to create a functional and user-friendly website.

* The core of the project is built with Django, chosen for its simplicity and the speed at which applications can be developed. Django's "batteries-included" philosophy allows for a wide range of functionalities to be included right out of the box, reducing the need for additional tools or libraries.

* The client-side scripting for the website is handled using JavaScript, a versatile language that enables interactive web pages and is an essential part of web applications. The use of JavaScript in this project provides basic functionality and enhances the user experience.

* In addition to JavaScript, jQuery, a fast, small, and feature-rich JavaScript library, is utilized. Although its use in this project is minimal, it simplifies tasks such as HTML document traversal and manipulation, event handling, and animation, making these tasks much easier with an easy-to-use API that works across a multitude of browsers.

* The website's layout and presentation are designed using the Jinja templating language. Jinja is a modern and designer-friendly templating language for Python, modeled after Django’s templates. It is fast, widely used, and secure, offering both sandboxed templates and a powerful optional automatic HTML escaping system for security.

* While the use of APIs was considered during the development process, it was ultimately decided against to maintain the project's simplicity and ensure a smooth learning curve. As I continue to expand my knowledge and skills in web development, the integration of APIs will be an area of focus in future projects.

#### In conclusion, this project is a testament to my growing skills as a web developer, demonstrating my ability to effectively use a variety of tools and languages to create a functional and user-friendly web application. It also reflects my decision-making process in choosing the most appropriate tools for the task at hand and my commitment to continuous learning and improvement..

## How to use
* clone the repo :  `https://github.com/PhuyalGaurav/crasber `
* Install django & pillow : `pip install django`->`pip install pillow`
* If you want a new database then: 
	* Delete the previous database : `del db.sqlite3` or `rm db.sqlite3`  
	* Create a new database : `python manage.py migrate`
* Create a super user (used for admin panel) : `python manage.py runserver`
* Run the server : `python manage.py runserver`
* Visit the site at: http://127.0.0.1:8000/   
* Visit the admin panel at: http://127.0.0.1:8000/admin

## Features
The web application developed using Django offers a variety of features designed to enhance user interaction and engagement. Here's a detailed look at these features:

1. **User Posts**: The default page of the website displays all the posts made by the user. This feature provides a personalized experience, allowing users to easily access and manage their content.

2. **Creating New Posts**: Users who are logged in have the ability to create new posts. This encourages active participation and content generation, fostering a vibrant and dynamic community.

3. **Profile Pages**: Each user has a dedicated profile page. Other users can visit these profile pages and choose to follow or unfollow the user. This feature facilitates the building of social connections within the platform.

4. **Following Page**: There is a "Following" page where posts made only by the people a user follows are displayed. This allows users to curate their content feed based on their preferences and interests.

5. **Pagination**: If there are more than 10 posts on a single page, pagination is implemented to organize the posts and improve navigation. This ensures a smooth and user-friendly browsing experience. (This feature is currently truned off but is usable if need be.)

6. **Post Editing**: Users can edit their posts without refreshing the entire page. This feature enhances the user experience by providing a seamless way to manage and update content.

7. **Liking and Unliking Posts**: Users can like and unlike posts. This interactive feature allows users to express their reactions to different posts and contributes to the overall engagement on the platform.

Each of these features has been carefully designed and implemented to create a user-friendly, interactive, and engaging web application. The application not only allows users to create and manage content but also facilitates social interaction and community building. It is a testament to the power of Django and the other technologies used in its development.

## How to contribute  
 Just send a normal Pull request i might accept.
