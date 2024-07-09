import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load your data
data = pd.read_csv('data/rentcrime_kaggle.csv')

states = data['state'].unique()
regions_by_state = {state: data[data['state'] == state]['cityname'].unique() for state in states}

# Streamlit UI
st.title('Community Analysis :closed_lock_with_key:')
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
                # Plotting Crime Rates
                    st.header(f'Race Demographics in {selected_region}, {selected_state}')
                    race_columns = ['racepctblack', 'racePctWhite', 'racePctAsian', 'racePctHisp']
                    race_data = filtered_data[race_columns].mean()
                    race_data.index = ['Black', 'White', 'Asian', 'Hispanic']
                
                    col3a, col3b = st.columns([2, 1])
                    with col3a:
                        for race, pct in race_data.items():
                            st.markdown(f"- **{race}**: {pct:.2f}%")

                    with col3b:
                        fig, ax = plt.subplots(figsize=(5, 3))
                        race_data.plot(kind='pie', ax=ax, colors=['black', '#FFE5B4', '#c9a437', '#a6631d'], startangle=90)
                        ax.set_ylabel('')  # Hide the y-label for a cleaner look
                        ax.set_facecolor('#e4e4e4')
                        fig.patch.set_facecolor('#e4e4e4')
                        st.pyplot(fig)
                        
        

            with col2:
                with st.container():
                # Plotting Race Demographics
                    st.header(f'Crime Rates in {selected_region}, {selected_state}')
                    crime_columns = ['murdPerPop', 'rapesPerPop', 'robbbPerPop', 'assaultPerPop', 'burglPerPop', 
                                    'larcPerPop', 'autoTheftPerPop', 'arsonsPerPop', 'ViolentCrimesPerPop', 'nonViolPerPop']
                    crime_data = filtered_data[crime_columns].mean()
                    crime_data.index =['Murder', 'Rape', 'Robbery', 'Assault', 'Burglery', 
                                    'Larceny', 'Auto Theft', 'Arsons', 'Violent Crimes', 'non Violent']
                    fig, ax = plt.subplots(figsize=(12, 7))
                    crime_data.sort_values().plot(kind='barh', ax=ax, color='salmon')
                    ax.set_title(f'Average Crime Rates in {selected_region}, {selected_state}', fontsize=16)
                    ax.set_xlabel('Average Incidents per Capita', fontsize=14)
                    ax.set_ylabel('Crime Type', fontsize=14)
                    ax.set_facecolor('#e4e4e4')
                    fig.patch.set_facecolor('#e4e4e4')
                    st.pyplot(fig)

            st.subheader(f"Crime Metrics for {selected_region}, {selected_state}")
            avg_crime_rate = crime_data.mean()
            highest_crime_type = crime_data.idxmax()
            lowest_crime_type = crime_data.idxmin()
            
            st.markdown(f"- **Average Crime Rate**: {avg_crime_rate:.2f} incidents per capita")
            st.markdown(f"- **Highest Crime Type**: {highest_crime_type} with {crime_data[highest_crime_type]:.2f} incidents per capita")
            st.markdown(f"- **Lowest Crime Type**: {lowest_crime_type} with {crime_data[lowest_crime_type]:.2f} incidents per capita")


            total_population = filtered_data['population'].iloc[0]
            median_income = filtered_data['medIncome'].iloc[0]
            
            st.subheader("Additional Metrics")
            col1, col2= st.columns(2)
            with col1:
                st.metric("Total Population", f"{total_population:,.0f}")
            with col2:
                st.metric("Median Household Income", f"${median_income:,.2f}")


# Show the raw data
if st.checkbox('Show raw data'):
    st.subheader('📄 Raw data')
    st.write(filtered_data)

st.markdown("---")
st.markdown("### Data Sources")
st.markdown("The home value data is sourced from https://www.zillow.com/research/data/.")
st.markdown("The market heat index data is sourced from https://www.zillow.com/research/data/.")
st.markdown("The rent and demographic data is sourced from https://www.kaggle.com/datasets/hieppham1341/apartment-rentals-merged-with-socio-economics-info.")





