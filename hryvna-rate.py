from datetime import date, timedelta
import requests
from requests.exceptions import HTTPError
import sys
import json

def daterange(start, end):
	for n in range(int((end - start).days)):
		yield start + timedelta(n)


def generate_date_list(year):
	# Start date of the year
	start = date(year, 1, 1)
	# End date is the next year
	end = date(year + 1, 1, 1)

	date_list = []
	for single_date in daterange(start, end):
		date_list.append(single_date.strftime('%Y%m%d'))

	return date_list


# Start request
data = []

# Read data from input 
currency = sys.argv[1]

# Generate date list for 2021 year
date_list = generate_date_list(2021)
for single_date in date_list:
	try:
		res = requests.get(f'https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?valcode={currency}&date={single_date}&json')
		res.raise_for_status()

		# Responce only contain one body, so take only it
		data.append(res.json()[0])
	except HTTPError as http_err:
		print(f'HTTP error: {http_err}')
	except Exception as err:
		print(f'Error: {err}')

with open(f'{currency}.json', 'w') as f:
	json.dump(data, f, indent=4, ensure_ascii=False)
