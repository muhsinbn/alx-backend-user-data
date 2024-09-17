## Introduction:

This project focuses on implementing Basic Authentication in a web application. Basic Authentication is a method for a web server to request user credentials (username and password) to authenticate a client before granting access to resources. The project covers essential aspects of building an authentication system, securely handling user credentials, and protecting resources through access control.

## Background Context
In this project, you will learn what the authentication process means and implement a Basic Authentication on a simple API.

In the industry, you should not implement your own Basic authentication system and use a module or framework that doing it for you (like in Python-Flask: [Flask-HTTPAuth)](https://intranet.alxswe.com/rltoken/rpsPy0M3_FJuCLGNPUbmvg). Here, for the learning purpose, we will walk through each step of this mechanism to understand it by doing.

### Resources
**Read or watch:**

* [REST API Authentication Mechanisms](https://intranet.alxswe.com/rltoken/ssg5umgsMk5jKM8WRHk2Ug)
* [Base64 in Python](https://intranet.alxswe.com/rltoken/RpaPRyKx1rdHgRSUyuPfeg)
* [HTTP header Authorization](https://intranet.alxswe.com/rltoken/WlARq8tQPUGQq5VphLKM4w)
* [Flask](https://intranet.alxswe.com/rltoken/Zes_6jyFTaaem1lG47oTjQ)
* [Base64 - concept](https://intranet.alxswe.com/rltoken/br6Rp4iMaOce6EAC-JQnOw)

### 0. Simple-basic-API                                                     mandatory

Download and start your project from this [archive.zip](https://intranet.alxswe.com/rltoken/2o4gAozNufil_KjoxKI5bA)

In this archive, you will find a simple API with one model: User. Storage of these users is done via a serialization/deserialization in files.

### Setup and start server
bob@dylan:~$ pip3 install -r requirements.txt
...
bob@dylan:~$
bob@dylan:~$ API_HOST=0.0.0.0 API_PORT=5000 python3 -m api.v1.app
 * Serving Flask app "app" (lazy loading)
...
bob@dylan:~$

### Use the API (in another tab or in your browser)
bob@dylan:~$ curl "http://0.0.0.0:5000/api/v1/status" -vvv
*   Trying 0.0.0.0...
* TCP_NODELAY set
* Connected to 0.0.0.0 (127.0.0.1) port 5000 (#0)
> GET /api/v1/status HTTP/1.1
> Host: 0.0.0.0:5000
> User-Agent: curl/7.54.0
> Accept: */*
> 
* HTTP 1.0, assume close after body
< HTTP/1.0 200 OK
< Content-Type: application/json
< Content-Length: 16
< Access-Control-Allow-Origin: *
< Server: Werkzeug/1.0.1 Python/3.7.5
< Date: Mon, 18 May 2020 20:29:21 GMT
< 
{"status":"OK"}
* Closing connection 0
bob@dylan:~$
