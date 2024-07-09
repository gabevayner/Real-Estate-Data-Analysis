import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# Load data
home_value_data = pd.read_csv('data/home_value.csv')
heat_index_data = pd.read_csv('data/market_heat.csv')

home_value_data = home_value_data[['RegionID', 'SizeRank', 'RegionName', 'RegionType', 'StateName'] + [col for col in home_value_data.columns if col.startswith(('2018', '2019', '2020', '2021', '2022', '2023', '2024'))]]
heat_index_data = heat_index_data[['RegionID', 'SizeRank', 'RegionName', 'RegionType', 'StateName'] + [col for col in heat_index_data.columns if col.startswith(('2018', '2019', '2020', '2021', '2022', '2023', '2024'))]]

states = home_value_data['StateName'].unique()
regions_by_state = {state: home_value_data[home_value_data['StateName'] == state]['RegionName'].unique() for state in states}

# Streamlit UI
st.title('Home Values and Market Heat Index :house::chart_with_upwards_trend:')

selected_state = st.selectbox('Select a State 📍', states)

if selected_state:
    # Region selection based on selected state
    regions = regions_by_state[selected_state]
    selected_region = st.selectbox('Select a Region', regions)

    if selected_region:
        # Filter data based on selected state and region
        filtered_home_value_data = home_value_data[(home_value_data['StateName'] == selected_state) & (home_value_data['RegionName'] == selected_region)]
        filtered_heat_index_data = heat_index_data[(heat_index_data['StateName'] == selected_state) & (heat_index_data['RegionName'] == selected_region)]

        if not filtered_home_value_data.empty and not filtered_heat_index_data.empty:
            # Prepare data for plotting
            filtered_home_value_data = filtered_home_value_data.set_index('RegionName').transpose().reset_index()
            filtered_home_value_data.columns = ['Date', selected_region]
            filtered_home_value_data = filtered_home_value_data[1:]  # Skip the first row which contains the RegionName
            filtered_home_value_data['Date'] = pd.to_datetime(filtered_home_value_data['Date'], errors='coerce')
            filtered_home_value_data.dropna(subset=['Date'], inplace=True)

            filtered_heat_index_data = filtered_heat_index_data.set_index('RegionName').transpose().reset_index()
            filtered_heat_index_data.columns = ['Date', selected_region]
            filtered_heat_index_data = filtered_heat_index_data[1:]  # Skip the first row which contains the RegionName
            filtered_heat_index_data['Date'] = pd.to_datetime(filtered_heat_index_data['Date'], errors='coerce')
            filtered_heat_index_data.dropna(subset=['Date'], inplace=True)

            # Create columns for side by side plots
            avg_price = filtered_home_value_data[selected_region].mean()
            max_price = filtered_home_value_data[selected_region].max()
            min_price = filtered_home_value_data[selected_region].min()
            latest_price = filtered_home_value_data[selected_region].iloc[-1]
            earliest_price = filtered_home_value_data[selected_region].iloc[0]
            price_change = latest_price - earliest_price
            price_change_percentage = (price_change / earliest_price) * 100

            
            # Create columns for side by side plots
            col1, col2 = st.columns(2)

            with col1:
                # Plotting Home Values Over Time
                st.header(f'Avg Home Values in {selected_region}')
                fig, ax = plt.subplots(figsize=(7, 5))
                sns.lineplot(data=filtered_home_value_data, x='Date', y=selected_region, marker='o', ax=ax)
                ax.set_title(f'Home Values in {selected_region} Over Time', fontsize=16)
                ax.set_xlabel('Date', fontsize=14)
                ax.set_ylabel('Home Value', fontsize=14)
                ax.grid(True)
                ax.set_facecolor('#e4e4e4')
                fig.patch.set_facecolor('#e4e4e4')
                st.pyplot(fig)
                
                

            with col2:
                # Plotting House Prices Distribution
                st.header(f'Price Distribution in {selected_region}')
                fig, ax = plt.subplots(figsize=(7, 5))
                sns.histplot(filtered_home_value_data[selected_region], kde=True, ax=ax, color='skyblue')
                ax.set_title(f'House Prices Distribution in {selected_region}', fontsize=16)
                ax.set_xlabel('House Price', fontsize=14)
                ax.set_ylabel('Frequency', fontsize=14)
                ax.set_facecolor('#e4e4e4')
                fig.patch.set_facecolor('#e4e4e4')
                st.pyplot(fig)

                
            with st.container():
                col1, col2, col3 = st.columns(3)
                col2.metric("Average Price", f"${avg_price:,.2f}")
                col1.metric("Highest Price", f"${max_price:,.2f}")
                col3.metric("Lowest Price", f"${min_price:,.2f}")

            
            with st.container():
                st.header("""MARKET HEAT INDEX""")
                st.write("""The market heat index is a time series dataset that aims to capture the balance of for-sale supply and 
                         demand in a given market. A higher number means the market is more tilted in favor of sellers. It relies on 
                         a combination of engagement and listing performance inputs to provide insights into current market dynamics.
                        :blue[It is calculated for single-family and condo homes.]""")


            # Plotting correlation between home values and market heat index
            st.header(f'Correlation of Home Values and Market Heat Index in {selected_region}')
            fig, ax1 = plt.subplots(figsize=(12, 6))
            ax1.set_title(f"Correlation of Home Values and Market Heat Index in {selected_region}")
            ax1.set_xlabel('Date')
            ax1.set_ylabel('Home Values', color='tab:blue')
            line1, = ax1.plot(filtered_home_value_data['Date'], filtered_home_value_data[selected_region], color='tab:blue', label='Home Values')
            ax2 = ax1.twinx()
            ax2.set_ylabel('Market Heat Index', color='tab:red')
            line2, = ax2.plot(filtered_heat_index_data['Date'], filtered_heat_index_data[selected_region], color='tab:red', label='Market Heat Index')
            fig.tight_layout()
            fig.legend(handles=[line1, line2], loc='upper left')
            st.pyplot(fig)

            # Aggregate Heat Index Data by State
            state_heat_index = heat_index_data.groupby('StateName').mean()

            # Heat Index Comparison for Selected States
            st.header("Average Market Heat Index Comparison by State (2018-2024)")
            fig, ax = plt.subplots(figsize=(14, 8))
            sns.barplot(x=state_heat_index.index, y=state_heat_index.mean(axis=1), ax=ax)
            ax.set_title("Average Market Heat Index Comparison by State (2018-2024)")
            ax.set_xlabel("State")
            ax.set_ylabel("Average Market Heat Index")
            plt.xticks(rotation=90)
            st.pyplot(fig)


            # Multi-select box for selecting states to compare
            selected_states = st.multiselect('Select states to compare:', states, default=states[1:4])

            # Line Plot for Heat Index Trends by State
            st.header("Market Heat Index Trends by Selected States (2018-2024)")
            fig, ax = plt.subplots(figsize=(14, 8))
            ax.set_title("Market Heat Index Trends by Selected States (2018-2024)")
            for state in selected_states:
                state_data = heat_index_data[heat_index_data['StateName'] == state].mean()
                ax.plot(state_data.index[5:], state_data.values[5:], label=state)
            ax.set_xlabel("Date")
            ax.set_ylabel("Market Heat Index")
            plt.legend(loc='upper left')
            plt.xticks(rotation=45)
            ax.xaxis.set_major_locator(plt.MaxNLocator(nbins=10))  # To make the x-axis ticks more readable
            st.pyplot(fig)

            # Show the raw data
            if st.checkbox('Show raw data'):
                st.subheader('Raw data')
                st.write(home_value_data)
                st.write(heat_index_data)

st.markdown("---")
st.markdown("### Data Sources")
st.markdown("The home value data is sourced from https://www.zillow.com/research/data/(#).")
st.markdown("The market heat index data is sourced from https://www.zillow.com/research/data/(#).")
st.markdown("The rent and demographic data is sourced from https://www.kaggle.com/datasets/hieppham1341/apartment-rentals-merged-with-socio-economics-info(#).")


