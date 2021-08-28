from datetime import datetime, timedelta
import pandas as pd 
from pandas import Timestamp
import yfinance as yf
import time

from Screener import db 
from Screener.models import *


# Helper function to create a visual progress bar for functions
def printProgressBar (i, total, prefix = '', decimals = 1, length = 100):

    percent = ("{0:." + str(decimals) + "f}").format(100 * (i / float(total)))
    filledLength = int(length * i // total)
    bar = '█' * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} [{bar}] {percent}%', end = '\r')

    # Print New Line on Complete
    if i == total: 
        print()


# Function to build the database from scratch
def buildDB():
    # reset the database
    db.drop_all()
    db.create_all()

    # Scrape the list of S&P 500 Companies
    table = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
    df = table[0]

    # Change format for the two tickers
    df.at[df.index[df['Symbol'] == 'BRK.B'], 'Symbol'] = 'BRK-B'
    df.at[df.index[df['Symbol'] == 'BF.B'], 'Symbol'] = 'BF-B'


    start_time = time.time()

    # Create the database entries for each sector, security, and industry and the relationships between them
    for i in df.index:
        symbol = df['Symbol'][i]
        security = df['Security'][i]
        sector = df['GICS Sector'][i]
        industry = df['GICS Sub-Industry'][i]

        sector_model = Sector.query.filter_by(sector = sector).first()
        industry_model = Industry.query.filter_by(industry = industry).first()

        # sector already added to the database
        if sector_model:

            # industry already added to the database
            if industry_model:
                pass
            # sector in the database but not the industry, create the industry
            else:
                industry_model = Industry(industry = industry, sector_id = sector_model.id, sector = sector_model)
                db.session.add(industry_model)
                db.session.commit()
           
        # sector isnt in the database, create the sector and industry
        else:
            sector_model = Sector(sector = sector)
            industry_model = Industry(industry = industry, sector_id = sector_model.id, sector = sector_model)
            db.session.add(sector_model)
            db.session.add(industry_model)
            db.session.commit()

        security_model = Security(symbol=symbol, security=security, industry_id = industry_model.id, industry = industry_model)
        db.session.add(security_model)
        db.session.commit()

        printProgressBar(i + 1, len(df), prefix='Creating models and relationships: ')

    end_time = time.time()
    delta = end_time - start_time
    print(f'Elapsed time: {delta:10.4} s')



    # Create historic data for all securities
    securities = Security.query.all()
    start_time = time.time()

    i = 0
    for security in securities:
        ticker = yf.Ticker(security.symbol)

        end = datetime.today()
        start = end - timedelta(days=365*5)
        df = ticker.history(start=start.strftime('%Y-%m-%d'), end=end.strftime('%Y-%m-%d'), interval='1d', actions=False)

        df.to_sql(security.symbol, db.engine, if_exists='replace')
        updateDeltas(security, df)

        printProgressBar(i + 1, len(securities), prefix='Fetching historic data: ')
        i = i + 1

    db.session.commit()
    end_time = time.time()
    delta = end_time - start_time
    print(f'Elapsed time: {delta:10.4} s')



# Function to update the database to the current date
def updateDB():
    securities = Security.query.all()
    start_time = time.time()
    i = 0


    # Update all the securities to reflect present day
    for security in securities:
        updateTable(security)

        printProgressBar(i + 1, len(securities), prefix='Updating historic data: ')
        i = i + 1

    db.session.commit()

    end_time = time.time()
    delta = end_time - start_time
    print(f'Elapsed time: {delta:10.4} s')


# Function to append new up to date data, and trim data over 5Y
def updateTable(security: 'Security') -> None:

    df = pd.read_sql_table(security.symbol, db.engine)

    # ending day should be today
    end = datetime.now()
    end = end.replace(hour=0, minute=0, second=0, microsecond=0)

    # If last value in table is equal to today, then all historic data is up to date
    if Timestamp.to_pydatetime(df.iloc[-1]['Date']) == end:
        return

    # starting day should be 5 years ago 
    start = end - timedelta(days=365*5)
    
    # Filter out original data frame of dates greater than 5 years ago
    df = df[df['Date'] > start]
    
    # Grab the last date in the data to start reading data for
    start = Timestamp.to_pydatetime(df.iloc[-1]['Date']) + timedelta(days=1)

    # grab the updated 
    ticker = yf.Ticker(security.symbol)
    yf_df = ticker.history(start=start.strftime('%Y-%m-%d'), end=end.strftime('%Y-%m-%d'), interval='1d', actions=False)
    yf_df = yf_df.reset_index()

    # append the new grabbed data to the original 
    df = pd.concat([df, yf_df], ignore_index=True)

    # update database with new data
    df.to_sql(security.symbol, db.engine, if_exists='replace')

    # update the security's delta values
    updateDeltas(security, df)


# Function to calculate the percent increase/decrease for each security
def updateDeltas(security: 'Security', df: 'pd.DataFrame') -> None:
    ONE_DAY_INDEX = -2 
    ONE_WEEK_INDEX = -5
    ONE_MONTH_INDEX = -21
    THREE_MONTH_INDEX = -21 * 3
    ONE_YEAR_INDEX = -5 * 52 
    THREE_YEAR_INDEX = -5 * 52 * 3
    FIVE_YEAR_INDEX = 0 

    # Calculate deltas
    end_price = df.iloc[-1]['Close']

    # One day
    start_price = df.iloc[ONE_DAY_INDEX]['Close']
    security.one_day_delta = (end_price - start_price)/start_price * 100
    
    # One Week
    if df.shape[0] > -1 * ONE_WEEK_INDEX:
        start_price = df.iloc[ONE_WEEK_INDEX]['Close']
        security.one_week_delta = (end_price - start_price)/start_price * 100
    else:
        start_price = df.iloc[0]['Close']
        security.one_week_delta = (end_price - start_price)/start_price * 100

    # One Month
    if df.shape[0] > -1 * ONE_MONTH_INDEX:
        start_price = df.iloc[ONE_MONTH_INDEX]['Close']
        security.one_month_delta = (end_price - start_price)/start_price * 100
    else:
        start_price = df.iloc[0]['Close']
        security.one_month_delta = (end_price - start_price)/start_price * 100

    # Three Month
    if df.shape[0] > -1 * THREE_MONTH_INDEX:
        start_price = df.iloc[THREE_MONTH_INDEX]['Close']
        security.three_month_delta = (end_price - start_price)/start_price * 100
    else:
        start_price = df.iloc[0]['Close']
        security.three_month_delta = (end_price - start_price)/start_price * 100

    # One Year
    if df.shape[0] > -1 * ONE_YEAR_INDEX:
        start_price = df.iloc[ONE_YEAR_INDEX]['Close']
        security.one_year_delta = (end_price - start_price)/start_price * 100
    else: 
        start_price = df.iloc[0]['Close']
        security.one_year_delta = (end_price - start_price)/start_price * 100

    # Three Year
    if df.shape[0] > -1 * THREE_YEAR_INDEX:
        start_price = df.iloc[THREE_YEAR_INDEX]['Close']
        security.three_year_delta = (end_price - start_price)/start_price * 100
    else:
        start_price = df.iloc[FIVE_YEAR_INDEX]['Close']
        security.three_year_delta = (end_price - start_price)/start_price * 100

    # Five Year
    start_price = df.iloc[0]['Close']
    security.five_year_delta = (end_price - start_price)/start_price * 100



if __name__ == '__main__':
    buildDB()