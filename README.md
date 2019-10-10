# DeepLab

This is a web application for streamlinng the management and analysis of
scientific samples.  

### THIS SOFTWARE IS CURRENTLY IN ACTIVE DEVELOPMENT


# Building the project 

## Initialize the project

To create a new virtual environment for the project files called _env_ , run  
```python3 -m venv env```  

To activate the virtual environment named _env_, navigate to project folder (```cd deeplab```) and run  
```source env/bin/activate```  

To deactivate, run  
```deactivate```  

To install Django, inside the environment run  
```pip install flask```  




# Database management

## Creation of data tables and models


# Using Git for version control
## Setup Git repository

To turn active folder into git repository, run  
```git init```  
```git add -A```  
```git commit -am "initial commit"```  

To send to a Github repository, run  
```git remote add origin https://github.com/ericmuckley/DeepLab.git```  
```git push -u origin master```  

## Push future updates to Github

For future pushes to Github, run  
```git add -A```  
```git commit -am "commit message"```  
```git push origin master```  


# Deploy the app

To test the app, navigate to the outter directory and run  
```flask run```  

Before deploying, change ```DEBUG = True``` to ```DEBUG = False``` in _settings.py_.  

To export a list of dependencies to a requirements file, run  
```pip freeze > requirements.txt```  

And to install all dependencies from requirements file, run  
```pip install -r requirements.txt```  

To add the Heroku app as a git remote for the first time, run  
```heroku git:remote -a yourappname```   

Finally to push to Heroku and deploy, run   
```git push heroku master```  









