# SoftDesk Support API

> ### ***Disclaimer :***
> *This project, including what is included in this README, is a school project responding to a 
> fictional scenario and has no other purpose.*

A REST API made using **_Django REST Framework_**.

## Installation

1. Clone the repository to your local machine
2. I strongly recommend to set up a virtual environment (poetry, pipenv, ...) For this example we will use poetry.  
You can find poetry documentation [here](https://python-poetry.org/docs/) if needed.
3. Activate your virtual environment and install the requirements. With poetry that would be:  
    ```
    poetry shell
    poetry install
    ```
4. Go in the main app *softdeskapi* and run the migrations with `python manage.py migrate`
5. The project is now ready to go but keep in mind you have no data yet at this point. So you'll have to first create  
a superuser with the usual `python manage.py createsuperuser`
6. To start the app run `python manage.py runserver`

## Quick endpoints overview

Excepted the endpoints used to get tokens, every endpoints will require an access token to be provided as a bearer token  
in authorization header. So you must have a line like `"Authorization": "Bearer {access_token}"` in your headers.

### [POST] : *<base_url>/api/token/*
Use to get authentication tokens for an user. The request body must provide the **username** and **password** of the user.  
The response contains the access token and the refresh token.  


### [POST] : *<base_url>/api/token/refresh/*
Use this endpoint to get a new access token.  
In the body, provide the refresh token under the **refresh** key to get a new **access** token.

### [GET] [POST] : *<base_url>/api/users/*
Use this endpoint to get a list of users or to create a new user.  
Admins only can create new users and see inactive ones.

### [PUT] [PATCH] [DEL] : *<base_url>/api/users/{pk}/*
Get details, update or delete an user are only available to the user himself or admins.

### [GET] [POST] : *<base_url>/api/projects/*
Use this endpoint to get all the projects where you are the author or a contributor. Or to create a new project.  
Admins not restricted.

### [PUT] [PATCH] [DEL] : *<base_url>/api/projects/{pk}/*
Author or read only. Admins not restricted.

### [GET] [POST] : *<base_url>/api/issues/*
Use this endpoint to get all the issues related to projects where you are the author or the contributor, or to create a new issue. Admins can see all issues.  
An issue can only be created in a project where you are author or contributor.  

### [PUT] [PATCH] [DEL] : *<base_url>/api/issues/{pk}/*
Author or read only. Admins not restricted.

### [GET] [POST] : *<base_url>/api/comments/*
Use this endpoint to see all comments you have made or related to issues of projects where you are a contributor (Admins can see all comments).   
Or to create a new comment (only if you are a contributor).

### [PUT] [PATCH] [DEL] : *<base_url>/api/comments/{pk}/*
Author or read only. Admins not restricted.