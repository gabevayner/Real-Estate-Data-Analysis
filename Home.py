import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import pydeck as pdk
from millify import millify

st.set_page_config(page_title="Home Page", page_icon=":house:", layout="wide", initial_sidebar_state="expanded")


@st.cache_data
def load_df():
    df = pd.read_csv('data/rentcrime_kaggle.csv')
    return df


# Streamlit app title
st.title("US Real Estate Data Analysis :house::earth_americas: ")

with st.container():

    col1,col2 = st.columns(2)

    df = pd.read_csv('data/home_value.csv')


    with col2:
        df = df.dropna(subset=['StateName'])

        # Aggregate data by state and compute average values
        state_avg_df = df.groupby('StateName').mean()

        # Calculate growth metrics based on the aggregated data
        state_avg_df['1yr Growth (%)'] = ((state_avg_df['2024-04-30'] - state_avg_df['2023-04-30']) / state_avg_df['2023-04-30']) * 100
        state_avg_df['5yr Growth (%)'] = ((state_avg_df['2024-04-30'] - state_avg_df['2019-04-30']) / state_avg_df['2019-04-30']) * 100
        state_avg_df['10yr Growth (%)'] = ((state_avg_df['2024-04-30'] - state_avg_df['2014-04-30']) / state_avg_df['2014-04-30']) * 100
        state_avg_df['All-time Growth (%)'] = ((state_avg_df['2024-04-30'] - state_avg_df['2000-01-31']) / state_avg_df['2000-01-31']) * 100

        # Calculate the average prices for each timeframe
        state_avg_df['Avg Price 2000'] = state_avg_df['2000-01-31']
        state_avg_df['Avg Price 2014'] = state_avg_df['2014-04-30']
        state_avg_df['Avg Price 2019'] = state_avg_df['2019-04-30']
        state_avg_df['Avg Price 2023'] = state_avg_df['2023-04-30']
        state_avg_df['Avg Price 2024'] = state_avg_df['2024-04-30']

        # Dropdown for state selection
        selected_state = st.selectbox("Select a State to view metrics:", state_avg_df.index)

        # Display metrics for the selected state
        if selected_state in state_avg_df.index:

            price_2000 = f"$"+millify(state_avg_df.loc[selected_state, 'Avg Price 2000'], precision=2)
            price_2014 = f"$"+millify(state_avg_df.loc[selected_state, 'Avg Price 2014'], precision=2)
            price_2019 = f"$"+millify(state_avg_df.loc[selected_state, 'Avg Price 2019'], precision=2)
            price_2023 = f"$"+millify(state_avg_df.loc[selected_state, 'Avg Price 2023'], precision=2)
            price_2024 = f"$"+millify(state_avg_df.loc[selected_state, 'Avg Price 2024'], precision=2)
            
            # Display growth percentages
            st.metric("1-Year Growth",price_2024, f"{state_avg_df.loc[selected_state, '1yr Growth (%)']:.2f}%")
            st.metric("5-Year Growth", price_2019, f"{state_avg_df.loc[selected_state, '5yr Growth (%)']:.2f}%")
            st.metric("10-Year Growth", price_2014, f"{state_avg_df.loc[selected_state, '10yr Growth (%)']:.2f}%")
            st.metric("24-Year Growth (All-time)", price_2000, f"{state_avg_df.loc[selected_state, 'All-time Growth (%)']:.2f}%")
        else:
            st.write(f"No data available for {selected_state}")

    highest_1yr_growth_state = state_avg_df['1yr Growth (%)'].idxmax()
    highest_1yr_growth_value = state_avg_df['1yr Growth (%)'].max()

    highest_5yr_growth_state = state_avg_df['5yr Growth (%)'].idxmax()
    highest_5yr_growth_value = state_avg_df['5yr Growth (%)'].max()

    highest_10yr_growth_state = state_avg_df['10yr Growth (%)'].idxmax()
    highest_10yr_growth_value = state_avg_df['10yr Growth (%)'].max()

    highest_all_time_growth_state = state_avg_df['All-time Growth (%)'].idxmax()
    highest_all_time_growth_value = state_avg_df['All-time Growth (%)'].max()

    st.markdown(f"""
        <p style="font-size: 20px;">
            <strong>Highest 1-Year Growth: </strong>{highest_1yr_growth_state} <span style="color: green;">({highest_1yr_growth_value:.2f}%)</span>
        </p>
        <p style="font-size: 20px;">
            <strong>Highest 5-Year Growth: </strong>{highest_5yr_growth_state} <span style="color: green;">({highest_5yr_growth_value:.2f}%)</span>
        </p>
        <p style="font-size: 20px;">
            <strong>Highest 10-Year Growth: </strong>{highest_10yr_growth_state} <span style="color: green;">({highest_10yr_growth_value:.2f}%)</span>
        </p>
        <p style="font-size: 20px;">
            <strong>Highest All-Time Growth: </strong>{highest_all_time_growth_state} <span style="color: green;">({highest_all_time_growth_value:.2f}%)</span>
        </p>
    """, unsafe_allow_html=True)







    with col1:

        st.map(load_df(),color='#2243B6',zoom=1.7)


st.markdown("---")
st.markdown("### Data Sources")
st.markdown("The home value data is sourced from https://www.zillow.com/research/data/(#).")
st.markdown("The market heat index data is sourced from https://www.zillow.com/research/data/(#).")
st.markdown("The rent and demographic data is sourced from https://www.kaggle.com/datasets/hieppham1341/apartment-rentals-merged-with-socio-economics-info(#).")



