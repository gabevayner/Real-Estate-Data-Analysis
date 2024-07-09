import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px

# Load your data
data = pd.read_csv('data/rentcrime_kaggle.csv')

states = data['state'].unique()
regions_by_state = {state: data[data['state'] == state]['cityname'].unique() for state in states}

# Streamlit UI
st.title('Rent Analysis :heavy_dollar_sign::house_buildings:')
selected_state = st.selectbox('Select a State', states)

if selected_state:
    # Region selection based on selected state
    regions = regions_by_state[selected_state]
    selected_region = st.selectbox('Select a Region', regions)

    if selected_region:
        # Filter data based on selected state and region
        filtered_data = data[(data['state'] == selected_state) & (data['cityname'] == selected_region)]

        if not filtered_data.empty:
            # Create columns for 2x2 grid layout
            col1, col2 = st.columns(2)

            with col1:
                with st.container():
                # Plotting Home Values Over Time
                    st.header(f'Apartment Rent in {selected_region}, {selected_state}')
                    fig, ax = plt.subplots(figsize=(10, 6))
                    sns.histplot(filtered_data['price'], kde=True, ax=ax, color='skyblue')
                    ax.set_title(f'Apartment Rent Prices in {selected_region}, {selected_state}', fontsize=16)
                    ax.set_xlabel('Rent Price', fontsize=14)
                    ax.set_ylabel('Frequency', fontsize=14)
                    ax.set_facecolor('#e4e4e4')
                    fig.patch.set_facecolor('#e4e4e4')
                    st.pyplot(fig)
                    

            with col2:
                with st.container():
                # Plotting House Prices Distribution
                    st.header(f'Price vs. Sqft in {selected_region}, {selected_state}')
                    fig, ax = plt.subplots(figsize=(10, 6))
                    sns.scatterplot(x=filtered_data['square_feet'], y=filtered_data['price'], ax=ax, color='blue')
                    ax.set_title(f'Price vs. Square Footage in {selected_region}, {selected_state}', fontsize=16)
                    ax.set_xlabel('Square Feet', fontsize=14)
                    ax.set_ylabel('Rent Price', fontsize=14)
                    ax.set_facecolor('#e4e4e4')
                    fig.patch.set_facecolor('#e4e4e4')
                    st.pyplot(fig)

            avg_price = filtered_data['price'].mean()
            max_price = filtered_data['price'].max()
            min_price = filtered_data['price'].min()
            avg_price_per_sqft = (filtered_data['price'] / filtered_data['square_feet']).mean()
            price_sqft_corr = filtered_data[['price', 'square_feet']].corr().iloc[0, 1]

            st.subheader("Metrics")
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Average Price", f"${avg_price:,.2f}")
                st.metric("Avg Price per SqFt", f"${avg_price_per_sqft:,.2f}")
            with col2:
                st.metric("Highest Price", f"${max_price:,.2f}")
                st.metric("Lowest Price", f"${min_price:,.2f}")
            with col3:
                st.metric("Price-SqFt Correlation", f"{price_sqft_corr:.2f}")


            with st.container():
                st.header("Zillow Observed Rent Index (ZORI)")
                st.write("""A smoothed measure of the typical observed market rate rent across a given region. 
                        ZORI is a repeat-rent index that is weighted to the rental housing stock to ensure representativeness 
                         across the entire market, not just those homes currently listed for-rent. The index is dollar-denominated 
                         by computing the mean of listed rents that fall into the 40th to 60th percentile range for all homes and 
                         apartments in a given region, which is weighted to reflect the rental housing stock.""")
                st.write(":blue[ZORI is created for three different categories: All homes, Single Family Residences, and Multi-Family Residences.]")
                    

                    

# Show the raw data
if st.checkbox('Show raw data'):
    st.subheader('📄 Raw data')
    st.write(filtered_data)

st.markdown("---")
st.markdown("### Data Sources")
st.markdown("The home value data is sourced from https://www.zillow.com/research/data/(#).")
st.markdown("The market heat index data is sourced from https://www.zillow.com/research/data/(#).")
st.markdown("The rent and demographic data is sourced from https://www.kaggle.com/datasets/hieppham1341/apartment-rentals-merged-with-socio-economics-info(#).")





