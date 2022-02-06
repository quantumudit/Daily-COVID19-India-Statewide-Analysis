
# Script to extract & cleanse current status data of COVID-19 in India by states #
# ============================================================================== #

# ------ Start of Program ----- #

import requests
import pandas as pd
from datetime import datetime, timezone, timedelta

DATA_URL = 'http://www.mohfw.gov.in/data/datanew.json'

response = requests.get(DATA_URL)
json_data = response.json()

all_states_covid_data = []

ist_timezone = timezone(timedelta(hours=5.5))
current_ist_timestamp = datetime.now(ist_timezone).strftime('%d-%b-%Y %H:%M:%S')

for item in json_data:
    state_code = item["state_code"]
    state_name = item["state_name"].replace('***','').strip()
    active = item["active"]
    positive = item["positive"]
    cured = item["cured"]
    death = item["death"]
    new_active = item["new_active"]
    new_positive = item["new_positive"]
    new_cured = item["new_cured"]
    new_death = item["new_death"]
    
    state_details = {
        'StateCode': state_code,
        'State Name': state_name,
        'Active Cases (Yesterday)': active,
        'Positive Cases (Yesterday)': positive,
        'Cured Cases (Yesterday)': cured,
        'Death Cases (Yesterday)': death,
        'Active Cases (Today)': new_active,
        'Positive Cases (Today)': new_positive,
        'Cured Cases (Today)': new_cured,
        'Death Cases (Today)': new_death,
        'Last Updated (IST)': current_ist_timestamp
    }
    
    if state_name != '':
        all_states_covid_data.append(state_details)
    else:
        continue

# Exporting data to flatfile #
# -------------------------- #

statewide_covid_df = pd.DataFrame(all_states_covid_data)
statewide_covid_df.to_csv('../02_DATA/india_statewide_daily_covid_data.csv', index=False)

# ------ End of Program ----- #