from request_parameters import *
#from db_keys import *
# from keys import *
from google.cloud.sql.connector import connector
import pg8000.native
import sqlalchemy
from datetime import date
from datetime import timedelta
import pandas as pd
import os


class GCP_PostGreSQL():
    def __init__(self, connectionName, user, password, db, top_companies_tickers):
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'creds.json'
        self.connectionName = connectionName
        self.user = user
        self.password = password
        self.db = db
        self.pool = sqlalchemy.create_engine(
            "postgresql+pg8000://",
            creator=self.getconn,
        )
        self.db_conn = self.pool.connect()
        self.top_companies_tickers = top_companies_tickers

    ###############################################################
    #getconn function will have the parameters of your GCP's postgresql instance.
    def getconn(self) -> pg8000.native.Connection:
        conn: pg8000.native.Connection = connector.connect(
            self.connectionName,
            "pg8000",
            user=self.user,
            password=self.password,
            db=self.db,
            enable_iam_auth=True
        ) # TODO DEBUG?
        return conn