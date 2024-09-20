## Introduction:
This project is about implementing Session Authentication in a web application. Unlike Basic Authentication, where credentials are sent with every request, Session Authentication stores user session data on the server side. This provides a more secure and scalable way of managing user authentication and access to resources.

Session Authentication involves creating a session when a user successfully logs in and using session cookies to authenticate users in subsequent requests. This project demonstrates how to implement this method in a Python-based web application using Flask.

### Background Context
In this project, you will implement a Session Authentication. You are not allowed to install any other module.

In the industry, you should not implement your own Session authentication system and use a module or framework that doing it for you (like in Python-Flask: [Flask-HTTPAuth](https://intranet.alxswe.com/rltoken/_ZTQTaMKjx1S_xATshexkA)). Here, for the learning purpose, we will walk through each step of this mechanism to understand it by doing.

### Resources
**Read or watch:**

* [REST API Authentication Mechanisms - Only the session auth part](https://intranet.alxswe.com/rltoken/oofk0VhuS0ZFZTNTVrQeaQ)
* [HTTP Cookie](https://intranet.alxswe.com/rltoken/peLV8xuJ4PDJMOVFqk-d2g)
* [Flask](https://intranet.alxswe.com/rltoken/yrCaeZxNcpagOLh-0SVhwA)
* [Flask Cookie](https://intranet.alxswe.com/rltoken/QYfI5oW6OHUmHDzwKV1Qsw)
