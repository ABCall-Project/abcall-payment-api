import os
from dotenv import load_dotenv

environment = os.getenv('FLASK_ENV')

if environment == 'local':
    load_dotenv(dotenv_path='.env.local')
else:
    load_dotenv(dotenv_path='.env')

class Config:
    ENVIRONMENT = environment
    APP_NAME=os.getenv('APP_NAME')
    DATABASE_URI=os.getenv('DATABASE_URI')
    SCHEDULE_BROKER=os.getenv('SCHEDULE_BROKER')
    TOPIC_SCHEDULE=os.getenv('TOPIC_SCHEDULE')
    MINUTES_TO_EXECUTE_INVOICES=os.getenv('MINUTES_TO_EXECUTE_INVOICES')
    URL_REPORTS_SERVICE=os.getenv('URL_REPORTS_SERVICE')
    ISSUE_API_PATH=os.getenv('ISSUE_API_PATH')