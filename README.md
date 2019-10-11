# DeepLab

This is a web application for management and analysis of
scientific samples.  

### THIS SOFTWARE IS CURRENTLY IN ACTIVE DEVELOPMENT


# Building the project 

## Initialize the project

To create a new virtual environment for the project files called _env_ , run  
```python3 -m venv venv```  

To activate the virtual environment named _env_, navigate to project folder (```cd deeplab```) and run  
```source venv/bin/activate```  

To deactivate, run  
```deactivate```  

To install Flask, inside the environment run  
```pip install flask```  




# Database management

To connect to an SQL database from the Flask app, install _flask-sqlalchemy_  
For database migrations, install _flask-migrate_  
To create a database for the first time, delete the _migrations_ folder, 
delete all _pycache_ folders, and run  
```flask db init```  
To migrate changes you made to the database models, run  
```flask db migrate```  
To apply the database changes, run  
```flask db upgrade```




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









