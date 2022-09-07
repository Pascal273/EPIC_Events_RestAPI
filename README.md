# Introduction
This is the 12th project for the Python path of Openclassrooms.
The goal is to develop a secure back-end architecture Using Django ORM.

# Required Setup to run the program:

1. Python version 3.10.5 or higher must be installed.
2. A PostgreSQL database must be available.
3. Create the directory in which you want to keep the program.
4. Open the the `settings.py`, go to DATABASES and change the information for
 your database accordingly.
   Example: 
    ```
        'NAME': '{database_name}',
        'USER': '{user_name}',
        'PASSWORD': '{database_password}',
        'HOST': '{host_address}',
        'PORT': '{port_number}',
   ```
6. Open your terminal.
7. Navigate to the folder that contains the `manage.py` and `requirements.txt` files
8. Create your Virtual Environment by running the command: `python -m venv venv`
9. Activate the environment by running: 
 `venv\Scripts\activate.bat` (Windows) 
 or `venv\Scripts\activate.ps1` (Powershell)
 or `source venv/bin/activate` (OS)
10. Install the requirements by running the command: `pip install -r requirements.txt`

# How to run the program:

1. Open your terminal
2. Navigate to the directory that contains the `manage.py` file
3. Activate the environment by running: 
 `venv\Scripts\activate.bat` (Windows) 
 or `venv\Scripts\activate.ps1` (Powershell)
 or `source venv/bin/activate` (OS)
4. Run the migrations to prepare the database and create the required teams in the following order:
    -  1. `python manage.py migrate authentication 0001`
    -  2. `python manage.py migrate api 0001`
    -  3. `python manage.py migrate authentication 0002`
5. Create the first admin-user (superuser):
    - Run `python manage.py createsuperuser`
    - Enter your credentials
    - You need these to sign in to the Admin-UI once the server is running.
6. Run the command: `python manage.py runserver` (Windows) or `python3 manage.py runserver`(Mac)
The default port is 8000. Add the port-number as a parameter to runserver to use a different
port to run the server. For Example: `python manage.py runserver 9000`

Steps 1-5 are only required for initial installation. For subsequent launches,
you only have to execute step 4 from the root folder of the project.

When the server is running after step 6 of the procedure, the Epic-Events-API can be 
accessed with your browser by pasting the URL: `http://127.0.0.1:8000/` 
or copy and paste the URL that is displayed in the Terminal.

The admin-user (Manager Team members) are able to access the Admin-UI at the URL:
`http://127.0.0.1:8000/admin`

# New Users
- New users can sign up by using the sign-up button on the api's home page in the browser.
- To sign up fill out the sign-up form and confirm by clicking the sign-up button.
- After signing up a new user can't log in to the api until his profile got activated.
- The new user must be activated by an admin (manager) by assigning him to a team.


### Technologies
- Django -version 4.0.5
- django-crispy-forms -version 1.14.0
- djangorestframework -version 3.13.1
- PostgreSQL -version 14.4

### Postman api-documentation:
https://www.postman.com/galactic-meadow-498703/workspace/d186603e-6a6e-4559-afcd-869cf67eed16/documentation/20098177-e45a0823-ec53-4979-a509-be53ac03ff0a
