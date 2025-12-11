"""
Class: CS230--Section 5
Name: Owen Hegarty
Description: This page of code is used for the recordholders page of my final project, where users can see some cool information
on the airports with the most extreme data, like highest/lowest elevation, and the country with the most airports.
I pledge that I have completed the programming assignment
independently.
I have not copied the code from a student or any source.
I have not given my code to any student.
"""

import streamlit as st
import pandas as pd

FILENAME = "airport-codes.csv"

df = pd.read_csv(FILENAME)

#Below code creates a function that can be used for anywhere in dataframe to find the maximum value
def get_record_holder(df, column, direction='max'): #[FUNC2P] #[FUNCCALL2]
    if direction == 'max':
        record_value = df[column].max() #[MAXMIN]
    elif direction == 'min':
        record_value = df[column].min() #[MAXMIN]

    #Filtering for airports with the record value
    record_holder_df = df[df[column] == record_value]

    return record_holder_df.iloc[0], record_value #[FUNCRETURN2]

def main():
    st.title("Recordholders Around The Globe🌎") #Code displayed on website
    st.header("Discover The Most Extreme Airports On Earth!")
    st.divider()

    highest_airport_row, max_elevation = get_record_holder(df, 'elevation_ft', direction='max') #[FUNCCALL2]

    st.subheader("🏔️ Highest Airport on Earth")
    #Below code displays record holder in easily identifiable manner
    st.metric(label="Maximum Elevation", value=f"{max_elevation:,.0f} feet") #[ST3]
    st.markdown(f"""
            * **Airport:** **{highest_airport_row['name']}** ({highest_airport_row['iata_code']})
            * **Location:** {highest_airport_row['municipality']}, {highest_airport_row['iso_country']}
            * **Continent:** NA """) #[ST3]

    st.divider()

    lowest_airport_row, min_elevation = get_record_holder(df, 'elevation_ft', direction='min') #[FUNCCALL2]

    st.subheader("⬇️ Lowest Airport on Earth")
    #Below code displays record holder in easily identifiable manner
    st.metric(label="Minimum Elevation", value=f"{min_elevation:,.0f} feet") #[ST3]
    st.markdown(f"""
            * **Airport:** **{lowest_airport_row['name']}** ({lowest_airport_row['iata_code']})
            * **Location:** {lowest_airport_row['municipality']}, {lowest_airport_row['iso_country']}
            * **Continent:** {lowest_airport_row['continent']}""") #[ST3]

    st.divider()
    #Below code groups by country and counts the names then finds the max
    global_country_counts = df.groupby('iso_country')['name'].count().sort_values(ascending=False) #[SORT]
    top_country_code = global_country_counts.idxmax()
    top_country_count = global_country_counts.max()

    st.subheader("🗺️ Country with the Most Airports")
    #Below code displays record holder in easily identifiable manner
    st.metric(label="Total Airports (All Types)", value=f"{top_country_count:,}")
    st.markdown(f"""
        * **Country:** **{top_country_code}**
        * **Comparison:** """)
    num_countries = st.slider("Number of Top Countries to Display", min_value=5, max_value=20, value=10) #[ST2]
    st.bar_chart(global_country_counts.nlargest(num_countries)) #[CHART2]

    st.divider()

if __name__ == '__main__':

    main()
