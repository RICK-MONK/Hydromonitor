
from os import environ
from os.path import abspath, dirname
from dotenv import load_dotenv

load_dotenv()  # load environment variables from .env if it exists.
basedir = abspath(dirname(__file__))

class Config(object):
    """Base Config Object"""
    

    FLASK_DEBUG                             = environ.get('DEBUG', 'False').lower() in ('true', '1', 't')
    SECRET_KEY                              = environ.get('SECRET_KEY', 'Som3$ec5etK*y')
    UPLOADS_FOLDER                          = environ.get('UPLOADS_FOLDER', 'uploads') 
    IMAGE_FOLDER                            = environ.get('IMAGE_FOLDER', 'images') 

    ENV                                     = environ.get('FLASK_ENV') 
    FLASK_RUN_PORT                          = environ.get('FLASK_RUN_PORT') 
    FLASK_RUN_HOST                          = environ.get('FLASK_RUN_HOST') 

    # MONGODB VARIABLES
    DB_USERNAME                             = environ.get('DB_USERNAME', 'root') 
    DB_PASSWORD                             = environ.get('DB_PASSWORD', 'pass') 
    DB_SERVER                               = environ.get('DB_SERVER', 'localhost') 
    DB_PORT                                 = environ.get('DB_PORT', '27017') 

    PROPAGATE_EXCEPTIONS                    = False
 
 
