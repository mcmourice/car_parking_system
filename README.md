# car_parking_system
This is a web-based car parking managed system initially developed for a popular shopping mall in Nairobi

Installing the Web Application

Before installing the application you need to have installed the following:
	Python: free download at https://www.python.org 
	Virtual environment
	Package manager known as pip
	Django
Note: When using a python application that uses external dependencies that you are installing with pip, it is good practice to use virtual environment.

Setting up your environment

When you are ready to install the application, create a new folder and navigate to it. In this folder set up a new virtual environment called env using the command line as follows:
$ python -m venv env
 
The command sets up a new virtual environment named env in the current working directory.

In the meantime, you should copy the project folder containing the web app (parking_system) to the same directory as the env virtual environment
 
Still on the current working directory, activate the virtual environment to make it ready for use as follows:
$ env/Scripts/activate
 
If the activation is successful, the virtual environment’s will become (env) at the beginning of the next command prompt.
 
The next step is to install the Django in the dedicated development workspace as follows:
(env) $ python -m pip install django

Next, navigate to the project directory using the cd command:
(env) cd ...............\parking_system
 
Start the Django web server using the following command line
(env) python manage.py runserver

In your browser, go to http://127.0.0.1:8000/ to access the web application login interface

Login as either administrator or cashier using the respective credentials:

By default:
Administrator username = mcmourice, password = django12345

After first-time login, admin can add the cashier user under the 'Manage system users' section in the panel
