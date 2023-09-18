import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt

# Define the correct username and password
CORRECT_USERNAME = 'nimai'
CORRECT_PASSWORD = 'iloverubin'

# Function to fetch data from World Bank API
def get_world_bank_data(country_code, indicator_code, start_date, end_date):
    url = f"http://api.worldbank.org/v2/country/{country_code}/indicator/{indicator_code}?date={start_date}:{end_date}&format=json"
    response = requests.get(url)
    data = response.json()
    return data[1]

# Function to fetch and display data for a specific country
def fetch_and_display_data(country_name, country_code, gdp_indicator_code, population_indicator_code, start_date, end_date):
    st.write(f'Data for {country_name}:')

    # Fetch GDP data
    gdp_data = get_world_bank_data(country_code, gdp_indicator_code, start_date, end_date)
    gdp_df = pd.DataFrame([(entry['date'], entry['value']) for entry in gdp_data], columns=['Year', 'GDP (trillion USD)'])
    st.write('GDP data (trillion USD):')
    st.write(gdp_df)

    # Fetch Population data
    population_data = get_world_bank_data(country_code, population_indicator_code, start_date, end_date)
    population_df = pd.DataFrame([(entry['date'], entry['value']) for entry in population_data], columns=['Year', 'Population (billions)'])
    st.write('Population data (billions):')
    st.write(population_df)

    # Plotting GDP and Population
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    ax1.plot(gdp_df['Year\n'], gdp_df['GDP (trillion USD)'], label=f'{country_name} GDP (trillion USD)')
    ax1.set_ylabel('GDP (trillion USD)')
    ax1.set_xlabel('Year')
    ax1.set_title('Comparison of GDP')
    ax1.legend()

    ax2.plot(population_df['Year'], population_df['Population (billions)'], label=f'{country_name} Population (billions)')
    ax2.set_ylabel('Population (billions)')
    ax2.set_xlabel('Year')
    ax2.set_title('Comparison of Population')
    ax2.legend()

    st.pyplot(fig)

# Main Streamlit app
st.title('Login Page')

# Get user input for username and password
username = st.text_input('Username:')
password = st.text_input('Password:', type='password')

# Check if the login button is pressed
if st.button('Login'):
    if username == CORRECT_USERNAME and password == CORRECT_PASSWORD:
        st.success('Login successful!')
        st.title('Comparison of United States and Indian Economy (Real-Time Data)')

        # Country information
        country_info = {
            'United States': {'country_code': 'USA', 'gdp_indicator': 'NY.GDP.MKTP.CD', 'population_indicator': 'SP.POP.TOTL'},
            'India': {'country_code': 'IND', 'gdp_indicator': 'NY.GDP.MKTP.CD', 'population_indicator': 'SP.POP.TOTL'}
        }

        # Display data for each country
        for country_name, info in country_info.items():
            fetch_and_display_data(country_name, info['country_code'], info['gdp_indicator'], info['population_indicator'], '2010', '2021')

    else:
        st.error('Invalid credentials. Please try again.')
