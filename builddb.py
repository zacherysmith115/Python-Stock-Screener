from datetime import datetime, timedelta
import pandas as pd 
import yfinance as yf
import time

from Screener import db 
from Screener.models import *

def printProgressBar (i, total, prefix = '', decimals = 1, length = 100):

    percent = ("{0:." + str(decimals) + "f}").format(100 * (i / float(total)))
    filledLength = int(length * i // total)
    bar = '█' * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} [{bar}] {percent}%', end = '\r')

    # Print New Line on Complete
    if i == total: 
        print()

# reset the database
db.drop_all()
db.create_all()



# Scrape the list of S&P 500 Companies
table = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
df = table[0]

# Grab the ticker, compnay name, sector, and industry
# df.to_csv('S&P500-Info.csv', index=False, columns=['Symbol', 'Security', 'GICS Sector', 'GICS Sub-Industry'])

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

    printProgressBar(i + 1, len(securities), prefix='Fetching historic data: ')
    i = i + 1
