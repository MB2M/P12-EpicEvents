*This repository hosts a project to achieve during my training OpenClassRooms.com*

This script was created on Python 3.9 and use the Django framework in its 3.2.2 version.
It also use django rest framework v3.12.4


## Installation

Download the files in the directories of your choice

### 1) Create a Virtual Environment :
 
Go to the directory where you downloaded files and run this command on your terminal:

    python3 -m venv env
    
Then, initialize it :
 
- On Windows, run:

        env\Scripts\activate.bat
    
- On Unix or MacOS, run:

        source env/bin/activate
        
For more information, refer to the python.org documentation :

<https://docs.python.org/3/tutorial/venv.html>
    
### 2) Install the requirements

Still on you terminal, with the environment activated, run the following command to install the required libraries
    
    pip install -r requirements

### 3) Start the server

Go to the litreview/ repository and start the server using command:

    python manage.py runserver

Server is now running on

    http://127.0.0.1:8000/

### 4) PostreSQL access

A defaut configuration is already setup into the the settings.py file.

Fill free to change it if you want.

### 5) Run the database migration

Run a database migration:

    py manage.py migrate
    
### 6) Create super user

First of all, create a superuser so you can manage the admin part and create a 'standard' admin for the application

    python manage.py createsuperuser

Then run (again):

    py manage.py migrate

### 7) Using the application

The application works only using the standard admin part of django:

    <http://127.0.0.1:8000/admin/>


### 8) Connect to the API

In order to connect to the API, you need to have a private access to the application delivered by an admin.

Sending a POST request to <http://127.0.0.1:8000/api/token/> with fields 'email' and 'password'
--> You will receive a token you have to send in every request <--

Add it as a bearer token in your request header

### 9) Api documentation

Api documentation is not realeased