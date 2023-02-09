import json
import os

from model import Coins

import pandas as pd
from dotenv import load_dotenv
from requests import Session
from sqlalchemy.ext.declarative import declarative_base

# environment variables
load_dotenv(os.getenv("PWD")+"/env.dev")

COINMARKETCAP_KEY = os.getenv("COINMARKETCAP_KEY")
URI_COINMARKETCAP = os.getenv("URI_COINMARKETCAP")

# create a check function validate data with pandas
def check_if_valid_data(df: pd.DataFrame) -> bool:
	
	if df.empty:
		print("\nDataframe empty. Finishing execution")
		return False

	if df.symbol.empty:
		raise Exception("\nSymbol is Null. Finishing execution")

	if df.price.empty:
		raise Exception("\nPrice is Null. Finishing execution")

	if df.data_added.empty:
		raise Exception("\nData added is Null. Finishing execution")

	return True

# create a function to load data in storage with pandas and sql
def load_data(table_name, coins_df, session_db, engine_db):
   
	if check_if_valid_data(coins_df):
		print("\nData valid, proceed to Load stage")
	
	try:
		coins_df.to_sql(table_name, engine_db, index=False, if_exists='append')
		print("\nData loaded successfully")
	except Exception as err:
		print("\nFail load data on database: {}".format(err))
	
	session_db.commit()
	session_db.close()
	print("\nClose database successfully")
	return coins_df

# create a function to get data from coinmarketcap api
def get_data(session_db, engine_db, start, limit, convert, key, url):
	# get data from api
	parameters = {
		'start': start,
		'limit': limit,
		'convert': convert
	}
	headers = {
		'Accepts': 'application/json',
		'X-CMC_PRO_API_KEY': key,
	}
	session = Session()
	session.headers.update(headers)
 
	name = []
	symbol = []
	data_added = []
	last_updated = []
	price = []
	volume_24h = []
	circulating_supply = []
	total_supply = []
	max_supply = []
	percent_change_1h = []
	percent_change_24h = []
	percent_change_7d = []
 
	try:
		response = session.get(url, params=parameters)
		data = json.loads(response.text)
		
		print('\n')
		for coin in data['data']:
			name.append(coin['name'])
			symbol.append(coin['symbol'])
			data_added.append(coin['date_added'])
			last_updated.append(coin['last_updated'])
			price.append(coin['quote'][convert]['price'])
			volume_24h.append(coin['quote'][convert]['volume_24h'])
			circulating_supply.append(coin['circulating_supply'])
			total_supply.append(coin['total_supply'])
			max_supply.append(coin['max_supply'])
			percent_change_1h.append(coin['quote'][convert]['percent_change_1h'])
			percent_change_24h.append(coin['quote'][convert]['percent_change_24h'])
			percent_change_7d.append(coin['quote'][convert]['percent_change_7d'])
   
		coin_dict = {
			"name": name,
			"symbol": symbol,
			"data_added": data_added,
			"last_updated": last_updated,
			"price": price,
			"volume_24h": volume_24h,
			# "volume_7d": volume_7d,
			# "volume_30d": volume_30d,
			"circulating_supply": circulating_supply,
			"total_supply": total_supply,
			"max_supply": max_supply,
			"volume_24h": volume_24h,
			"percent_change_1h": percent_change_1h,
			"percent_change_24h": percent_change_24h,
			"percent_change_7d": percent_change_7d
		}
	except Exception as e:
		print(f'Error to get data from API: {e}')
		exit(1)
	
	# convert json to pandas
	coins_df = pd.DataFrame(coin_dict, columns=["name", "symbol", "data_added", "last_updated", "price", "volume_24h", "circulating_supply", "total_supply", "max_supply", "percent_change_1h", "percent_change_24h", "percent_change_7d"])
	print("Data on Pandas Dataframe:\n")
	print(coins_df.head(100))
	# convert pandas to sql
	load_data('tb_coins', coins_df, session_db, engine_db)

# Declaration base
Base = declarative_base()

# Make the coin table
get_session_db, get_engine = Coins.start()

# call the get_data function and load data on database
get_data(get_session_db,
         get_engine,
         '1',
         '5000',
         'USD',
         COINMARKETCAP_KEY,
         URI_COINMARKETCAP
         )

