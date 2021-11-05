
# Script to extract & cleanse current status data of COVID-19 in India by states #
# ============================================================================== #

# ------ Start of Program ----- #

import requests
import pandas as pd
import datetime

DATA_URL = 'http://www.mohfw.gov.in/data/datanew.json'

response = requests.get(DATA_URL)
json_data = response.json()


raw_data = pd.json_normalize(json_data)

states_filter = (raw_data['state_name'] != '')

raw_data_1 = raw_data[states_filter]

new_cols = [
    'SNo.',
    'State Name',
    'Active Cases (Yesterday)',
    'Positive Cases (Yesterday)',
    'Cured Cases (Yesterday)',
    'Death Cases (Yesterday)',
    'Active Cases (Today)',
    'Positive Cases (Today)',
    'Cured Cases (Today)',
    'Death Cases (Today)',
    'StateCode'
]

raw_data_1.columns = new_cols

reordered_cols = [
    'SNo.',
    'StateCode',
    'State Name',
    'Active Cases (Yesterday)',
    'Positive Cases (Yesterday)',
    'Cured Cases (Yesterday)',
    'Death Cases (Yesterday)',
    'Active Cases (Today)',
    'Positive Cases (Today)',
    'Cured Cases (Today)',
    'Death Cases (Today)'
]

raw_data_2 = raw_data_1.reindex(columns = reordered_cols)
raw_data_3 = raw_data_2.set_index('SNo.')

# Adding current date time to show a last-updated column:

current_datetime = datetime.datetime.now(datetime.timezone.utc)
formatted_datetime = current_datetime.strftime('%d-%b-%Y %H:%M:%S')

raw_data_3['Last Updated (UTC)'] = formatted_datetime

clean_data = raw_data_3.sort_index()

# Dumping data into a csv file:

clean_data.to_csv('../02_DATA/india_statewide_daily_covid_data.csv', index=True)

# ------ End of Program ----- #