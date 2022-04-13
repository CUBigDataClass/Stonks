

from google.cloud.sql.connector import connector
import pg8000.native
import sqlalchemy
import yfinance as yf
from datetime import *
import pandas as pd
import os
import time
from google.cloud import storage
from postGres import *
from companies import *
from db_keys import *
from keys import *
import json


class stocks:

    def __init__(self,pg1):
        self.pg=pg1
        #os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = '../../creds.json'

    #Function to get the information of Companies which will return a dictionary
    def get_company_info(self, ticker):
        """
        Function that gets the information of companies.
        Information such as Symbol, Name, Sector, Exchange, Website and Zip code of the company
        ***IMPORTANT: This function is to be run only once to get the information of all the companies in the Database. Once the information is stored in the database, it does not need to be updated.
        """
        stock_info = yf.Ticker('{}'.format(ticker)).info
        company={}
        company['Company_Symbol'] = stock_info['symbol']
        company['Company_Name'] = stock_info['shortName']
        company['Sector'] = stock_info['sector']
        company['Exchange'] = stock_info['exchange']
        company['Website'] = stock_info['website']
        return company

        """
        self.companies_info[ticker] = {}
        self.companies_info[ticker]['Company_Symbol'] = stock_info['symbol']
        self.companies_info[ticker]['Company Name'] = stock_info['shortName']
        self.companies_info[ticker]['Sector'] = stock_info['sector']
        self.companies_info[ticker]['Exchange'] = stock_info['exchange']
        self.companies_info[ticker]['Website'] = stock_info['website']
        """
        #there are cases where zip is not there, so set it as null if it doesn't exist
        #e.g. '0941.HK'
        """
        if(stock_info['zip']):
            self.companies_info[ticker]['Zip'] = stock_info['zip']
        else:
            self.companies_info[ticker]['Zip'] = "null"
        """
        #print(stock_info['shortName'])

    def get_top_companies_info(self):
        "Function that calls `get_company_info` for each top companies"
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'creds.json'
        bucket_name = 'stonksbucket'
        destination_blob_name = 'companies'
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(destination_blob_name)

        with self.pg.pool.connect() as db_conn:
            for ticker in self.pg.top_companies_tickers:
                info=self.get_company_info(ticker)
                #print('{} Company Information Retrieved'.format(ticker))
                #print(info)
                symbol=info['Company_Symbol']
                name=info['Company_Name']
                sector=info['Sector']
                exchange=info['Exchange']
                website=info['Website']
                #print(symbol,name,sector,exchange,website)
                statement = """ INSERT INTO companies(company_ticker, company_name, sector, exchange, website) VALUES (%s,%s,%s,%s,%s)"""
                db_conn.execute(statement, (symbol,name,sector,exchange,website))
                blob.upload_from_string(json.dumps(info))

            #to_csv file is needed for converting dataframe to byte
            #self.companies_info.to_sql('company_information', con=db_conn, if_exists='replace')
            #query = """ALTER TABLE company_information ADD PRIMARY KEY ("Company_Symbol");"""
            #db_conn.execute(query)
    """
    #deprecated. Chose to create a table and insert due to error
    def create_prices_table(self,ticker):
        """"""
        Create a daily prices table in the database.
        This function essentially takes in a company symbol as the input, generates a price_history dataframe and then builds a table of daily prices
        using that dataframe.
        So, we don't have to manually create the columns.
        A Query is also being run which makes the company symbol and date as the primary keys.
        ***IMPORTANT: This function is to be run only once to create the daily_prices table in the database and fill it with the historical stock prices of one company.
        Once the data is in the table, it does not to be updated since all of this is historical data.
        """"""
        price_history = yf.Ticker('{}'.format(ticker)).history(period='1y', interval='1d')
        #some formatting
        price_history = price_history.reset_index()
        price_history['symbol'] = '{}'.format(ticker)
        price_history =price_history.drop(['Stock Splits'], axis=1)
        price_history['Date'] = pd.to_datetime(price_history['Date']).dt.strftime('%Y-%m-%dT%H:%M:%SZ') # TODO check isoformort
        return price_history

        ###############################################################
        ### Init db for prices and get history
    """
    """
    #deprecated. Chose to create a table and insert due to error
    def create_all_prices_table(self):
        #Call create_prices_table for all top companies.
        #Run one time only.
        
        #print("Creating all prices table")
        with self.pg.pool.connect() as db_conn:
            for ticker in self.pg.top_companies_tickers:
                price_history = self.create_prices_table(ticker)
                price_history.to_sql('daily_prices', con=db_conn, if_exists='replace', index=False)
                # creating company symbol as the primary key
                query = """"""ALTER TABLE daily_prices ADD PRIMARY KEY ("symbol","Date");""""""
                db_conn.execute(query)
                print('Daily prices table created')
    """

    ###############################################################
    # Querying func?
    def query_company_information(self):
        with self.pg.pool.connect() as db_conn:
            result = db_conn.execute("select * from company_information")
            for row in result:
                print(row)
    #Query to retrive values from the daily_prices table in the database.
    def query_daily_prices(self):
        with self.pg.pool.connect() as db_conn:
            result = db_conn.execute("select * from daily_prices")
            for row in result:
                print(row)

    ###############################################################
    ###
    def insert_historical_prices(self,ticker):
        """
        Inserts the historical prices of all the top 100 companies into the db.
        The function takes input as a company symbol, generates a price_history dataframe, does some formatting and then inserts the rows of that
        dataframe into the daily_prices table.
        ***IMPORTANT: This function is to be run only once to insert all the historical stock data of all the companies.
        Once the data is inserted, that data is not to be updated.
        """
        price_history = yf.Ticker('{}'.format(ticker)).history(period='1y', interval='1d')
        price_history = price_history.fillna(0)
        #some formatting
        price_history = price_history.reset_index()
        price_history['symbol'] = '{}'.format(ticker)
        price_history = price_history.drop(['Stock Splits'], axis=1)
        price_history['Date'] = pd.to_datetime(price_history['Date']).dt.strftime('%Y-%m-%dT%H:%M:%SZ')
        return price_history

    def insert_all_historical_prices(self):
        """ Calls insert_all_historical_prices"""
        #bucket configuration for stocks blob
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'creds.json'
        bucket_name = 'stonksbucket'
        destination_blob_name = 'stocks'
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(destination_blob_name)

        with self.pg.pool.connect() as db_conn:
            #deleting all before adding data to ensure 1 primary key
            #self.delete_price_data()
            #Adding historical prices of 8 companies.
            for ticker in self.pg.top_companies_tickers:
                price_history = self.insert_historical_prices(ticker)
                size=price_history.shape[0]
                for rows in range(size):
                    row=price_history.loc[rows]
                    date=row['Date']
                    date=date[:10]+" "+date[11:19]
                    open=row['Open']
                    high=row['High']
                    low=row['Low']
                    close=row['Close']
                    volume=row['Volume']
                    dividends=row['Dividends']
                    symbol=row['symbol']
                    #print(symbol,date,open,high,low,close,volume,dividends)
                    #print(type(date))

                    statement = """ INSERT INTO stocks(date, company_ticker, open, high, low, close, volume, dividends) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"""
                    db_conn.execute(statement, (date,symbol,open,high,low,close,volume,dividends))

                #print(price_history.shape[0])
                #price_history.to_sql('daily_prices', con=db_conn, if_exists='append', index=False)
                #to_csv function is needed to change dataframe format in to bytes for bucket
                #blob.upload_from_string(price_history.to_csv())
                print("{} Historical Data added".format(ticker))



    ###############################################################
    ###

    def insert_latest_stock_data(self,ticker,today,yesterday):
        """
        This function generates the latest stock data for the ticker of the company passed into the function.
        It will take yesterday's date as the starting date and today's date as the ending date to generate the latest stock data for every day.
        Once it generates the latest stock data, it will then append that row into the daily_prices table.
        ***IMPORTANT: This is the function that has to be run on a daily basis to keep the daily_prices table updated with the stock data of every company.
        """

        price_history = yf.Ticker('{}'.format(ticker)).history(start = '{}'.format(yesterday), end='{}'.format(today))
        #some formatting
        price_history = price_history.reset_index()
        price_history['symbol'] = '{}'.format(ticker)
        price_history = price_history.drop(['Stock Splits'], axis=1)
        price_history['Date'] = pd.to_datetime(price_history['Date']).dt.strftime('%Y-%m-%dT%H:%M:%SZ')
        return price_history

    def insert_all_latest_stock_data(self):
        bucket_name = 'stonksbucket'
        destination_blob_name = 'stocks'
        storage_client = storage.Client()
        bucket = storage_client.bucket(bucket_name)
        blob = bucket.blob(destination_blob_name)
        dupecheck=0
        count=0
        last_date=None
        with self.pg.pool.connect() as db_conn:
            size_query = db_conn.execute("""SELECT * FROM stocks""")
            size = db_conn.execute(size_query)
            for row in size:
                count+=1

            if (count==0):
                self.insert_all_historical_prices()

            else:
                today = date.today()
                #print(today)
                #yesterday = today - timedelta(days = 1)
                for ticker in self.pg.top_companies_tickers:
                    #print(ticker)
                    date_query = db_conn.execute("""select * from stocks where company_ticker='""" + ticker + """'   ORDER BY date DESC LIMIT 1""")
                    last_date=date_query.first()[0]
                    #print("last_date"+str(last_date))
                    last_date=last_date.strftime("%Y-%m-%d")
                    #print(last_date)
                    dupecheck=0
                    #check if we haven't ran the function today
                    if today!=last_date:
                        price_history = self.insert_latest_stock_data(ticker, today,last_date)
                        #print(price_history)
                        row_count=len(price_history.index)
                        for x in range(row_count):
                            dupecheck=0
                            row=price_history.loc[x]
                            curr_date = row['Date']
                            #print("currdate: "+curr_date)
                            #curr_date = curr_date[:10] + " " + curr_date[11:19]
                            open = row['Open']
                            high = row['High']
                            low = row['Low']
                            close = row['Close']
                            volume = row['Volume']
                            dividends = row['Dividends']
                            symbol = row['symbol']
                            check="""select * from stocks where company_ticker='"""+ticker+"""' AND date='"""+curr_date+"""'"""
                            initcheck=db_conn.execute(check)
                            #str_date=curr_date.strftime('%Y-%m-%dT%H:%M:%SZ')
                            for row in initcheck:
                                dupecheck+=1

                            if dupecheck==0:
                                statement = """ INSERT INTO stocks(date, company_ticker, open, high, low, close, volume, dividends) VALUES (%s,%s,%s,%s,%s,%s,%s,%s)"""
                                db_conn.execute(statement, (curr_date, symbol, open, high, low, close, volume, dividends))

                                print("{} Stock Data for {} added".format(ticker,curr_date))
                                #price_history.to_sql('daily_prices', con=db_conn, if_exists='append', index=False)
                                "Latest Stock Prices Inserted"
                                #insert in to bucket
                                blob.upload_from_string(price_history.to_csv())
                            else:
                                #print(dupecheck)
                                print("dupekey exists")

                            time.sleep(1)
                    else:
                        print("function already ran today")
            #print(price_history)

    def delete_price_data(self):
        with self.pg.pool.connect() as db_conn:
            string1="DELETE from daily_prices"
            db_conn.execute(string1)


    ###############################################################
    def plot_prices_df(self, ticker, Date):
        prices_df = self.get_prices_df_query()
        prices_df.loc[[ticker]][Date].plot()

    #Get/Querying from the database and storing it into another database.
    def get_prices_df_query(self):
        with self.pg.pool.connect() as db_conn:

            prices_df = pd.read_sql('daily_prices', db_conn, index_col=['symbol', 'Date'])

            return prices_df

#run this file every day
#update daily, starting from the nxt day since initialization of db
if __name__ == "__main__":
    #The credential path will be where the json file of secret keys is stored on your machine.
    #credential_path = "<File Path to where the json file of secret keys is stored in your local machine>"

    credential_path='creds.json'
    os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = credential_path
    pg = GCP_PostGreSQL(con_name, user, pw, db, tickers)
    st=stocks(pg)
    st.insert_all_latest_stock_data()



    #st.get_company_info('AAPL')
    #st.create_all_prices_table() '# TODO/DEBUG only if first init call
    #st.insert_all_historical_prices()
    #st.query_company_information()

    #gcp_pgsql = GCP_PostGreSQL(CONNECTION_NAME, USER, PASSWORD, DB, top_companies_tickers=TICKERS)
    # Set of DB and Get price history
    #gcp_pgsql.create_all_prices_table() # TODO/DEBUG only if first init call
    # [DAILY] Get lastest prices
    #gcp_pgsql.insert_all_historical_prices()
