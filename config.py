import os 
basedir = os.path.abspath(os.path.dirname(__file__))

# might not use this in this application but it's good to have as a precaution. 

class Config(): 
    SECRET_KEY = os.environ.get('SECRET_KEY') or "random_acts_of_kindness!!36"
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
    SQLALCHEMY_TRACK_MODIFICATIONS = False # silence time deprecation warnings