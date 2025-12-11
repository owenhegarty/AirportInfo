"""
Class: CS230--Section 5
Name: Owen Hegarty
Description: This page showcases the code used to help a user find airports around the world. They can enter search terms to find
a certain airport around the world and some key information about it, including where it is and the elevation of it.
I pledge that I have completed the programming assignment
independently.
I have not copied the code from a student or any source.
I have not given my code to any student.
"""

import streamlit as st
import pandas as pd

FILENAME = "airport-codes.csv"

def main():
    df = pd.read_csv(FILENAME)
    #Below code outputted for streamlit page
    st.title("Airport Finder🔎")
    st.divider()
    st.header("Search For An Airport You Know!")
    st.text("Once you type the name of your airport you will find:\n-Where It Is\n-What Type Of Airport It is\n-The Elevation Of The Airport")
    #Creating a text input for users to enter a city a term that coincides with the airport they're looking for, placeholder term found through streamlit "text input info"
    search_term = st.text_input(
        "Start typing the airport name or code here:",
        placeholder="e.g., 'JFK', 'La Guardia', or 'Newark'")

    if search_term:
        term = search_term.lower() #setting term to lowercase to make it easier to find
        #Below code creates a dataframe with terms that match user input, "|" operator found through pandas and Stack Overflow search, https://stackoverflow.com/questions/24775648/element-wise-logical-or-in-pandas
        results_df = df[
            (df['name'].str.lower().str.contains(term, na=False)) |
            (df['municipality'].str.lower().str.contains(term, na=False)) |
            (df['iata_code'].str.lower().str.contains(term, na=False)) |
            (df['gps_code'].str.lower().str.contains(term, na=False))].copy()
        if not results_df.empty: #Displays results once user enters a term
            st.success(f"Found {len(results_df)} result(s) matching '{search_term}'.")
            st.dataframe(
                results_df[[
                    'name',
                    'municipality',
                    'iso_country',
                    'type',
                    'elevation_ft']].rename(columns={
                    'name': 'Airport Name',
                    'municipality': 'Location (City)',
                    'iso_country': 'Country',
                    'type': 'Type',
                    'elevation_ft': 'Elevation (ft)'}),
                hide_index=True)
        else: #Displaying a warning message when there are no matchign terms
            st.warning(f"No airports found matching '{search_term}'. Please retry your search.") #[ST3]

if __name__ =='__main__':

    main()

