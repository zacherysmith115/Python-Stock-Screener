import pandas as pd 
from Screener import db 
from Screener.models import Security

# reset the database
db.drop_all()
db.create_all()

# Scrape the list of S&P 500 Companies
table = pd.read_html('https://en.wikipedia.org/wiki/List_of_S%26P_500_companies')
df = table[0]

# Grab the ticker, compnay name, sector, and industry
# df.to_csv('S&P500-Info.csv', index=False, columns=['Symbol', 'Security', 'GICS Sector', 'GICS Sub-Industry'])

dictionary = {}
entries = []
for i in df.index:
    symbol = df['Symbol'][i]
    security = df['Security'][i]
    sector = df['GICS Sector'][i]
    industry = df['GICS Sub-Industry'][i]

    if sector in dictionary:
        if industry in dictionary[sector]:
            pass
        else:
           dictionary[sector].append(industry)
    else:
        dictionary[sector] = []
        dictionary[sector].append(industry)

    entries.append(Security(symbol=symbol, security=security, sector=sector, industry=industry))
    

for entry in entries:
    db.session.add(entry)
    print(entry)

db.session.commit()