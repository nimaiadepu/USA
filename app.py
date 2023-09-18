import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt

# Function to fetch data from World Bank API
def get_world_bank_data(country_code, indicator_code, start_date, end_date):
    url = f"http://api.worldbank.org/v2/country/{country_code}/indicator/{indicator_code}?date={start_date}:{end_date}&format=json"
    response = requests.get(url)
    data = response.json()
    return data[1]

st.title('Comparison of United States and Indian Economy (Real-Time Data)')

# Fetch GDP data
us_gdp_data = get_world_bank_data('USA', 'NY.GDP.MKTP.CD', '2010', '2021')
india_gdp_data = get_world_bank_data('IND', 'NY.GDP.MKTP.CD', '2010', '2021')

us_gdp = pd.DataFrame([(entry['date'], entry['value']) for entry in us_gdp_data], columns=['Year', 'GDP (trillion USD)'])
india_gdp = pd.DataFrame([(entry['date'], entry['value']) for entry in india_gdp_data], columns=['Year', 'GDP (trillion USD)'])

# Fetch Population data
us_population_data = get_world_bank_data('USA', 'SP.POP.TOTL', '2010', '2021')
india_population_data = get_world_bank_data('IND', 'SP.POP.TOTL', '2010', '2021')

us_population = pd.DataFrame([(entry['date'], entry['value']) for entry in us_population_data], columns=['Year', 'Population (billions)'])
india_population = pd.DataFrame([(entry['date'], entry['value']) for entry in india_population_data], columns=['Year', 'Population (billions)'])

# Display the data
st.write('Data used for comparison:')
st.write('GDP data (trillion USD):')
st.write(us_gdp)
st.write(india_gdp)
st.write('Population data (billions):')
st.write(us_population)
st.write(india_population)

# Plotting GDP and Population
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

ax1.plot(us_gdp['Year'], us_gdp['GDP (trillion USD)'], label='US GDP (trillion USD)')
ax1.plot(india_gdp['Year'], india_gdp['GDP (trillion USD)'], label='India GDP (trillion USD)')
ax1.set_ylabel('GDP (trillion USD)')
ax1.set_xlabel('Year')
ax1.set_title('Comparison of GDP')
ax1.legend()

ax2.plot(us_population['Year'], us_population['Population (billions)'], label='US Population (billions)')
ax2.plot(india_population['Year'], india_population['Population (billions)'], label='India Population (billions)')
ax2.set_ylabel('Population (billions)')
ax2.set_xlabel('Year')
ax2.set_title('Comparison of Population')
ax2.legend()

st.pyplot(fig)
