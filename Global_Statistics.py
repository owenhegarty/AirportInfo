"""
Class: CS230--Section 5
Name: Owen Hegarty
Description: This code is used for the Global Statistics page on the website, where users can find information on the types
of airports around the world, including how many there are and where they are.
I pledge that I have completed the programming assignment
independently.
I have not copied the code from a student or any source.
I have not given my code to any student.
"""

import streamlit as st
import pandas as pd
import pydeck as pdk
import matplotlib.pyplot as plt

FILENAME = 'airport-codes.csv' #Setting symbolic constant

def identify_data(filename):
    df = pd.read_csv(filename)

    #Below code assigns longitude and latitude values with no errors
    df[['longitude', 'latitude']] = df['coordinates'].str.split(', ', expand=True)
    df['longitude'] = pd.to_numeric(df['longitude'], errors='coerce')
    df['latitude'] = pd.to_numeric(df['latitude'], errors='coerce')
    df.drop('coordinates', axis=1, inplace=True) #[COLUMNS]

    #Below code creates dataframes for each type of airport, to be used in later code (Mapping)
    open_airports_df = df[df['type'] != 'closed'].copy() #[FILTER1]
    closed_airports_df = df[df['type'] == 'closed'].copy() #[FILTER1]
    small_airports_df = df[df['type'] == 'small_airport'].copy() #[FILTER1]
    medium_airports_df = df[df['type'] == 'medium_airport'].copy() #[FILTER1]
    large_airports_df = df[df['type'] == 'large_airport'].copy() #[FILTER1]
    heliports_df = df[df['type'] == 'heliport'].copy() #[FILTER1]
    seaports_df = df[df['type'] == 'seaplane_base'].copy() #[FILTER1]
    balloonports_df = df[df['type'] == 'balloonport'].copy() #[FILTER1]
    num_airport_types = df['type'].value_counts()

    return open_airports_df, closed_airports_df, small_airports_df, medium_airports_df, large_airports_df, heliports_df, seaports_df, balloonports_df, num_airport_types #[FUNCRETURN2]

#Below function is used to assign colors for the 'open airports' map
def get_color(row):
    #Making large airport dots red
    if row['type'] == 'large_airport':
        return [255, 0, 0, 255]
    #Making medium airport dots green
    elif row['type'] == 'medium_airport':
        return [0, 255, 0, 255]
    #Making small airport dots blue
    elif row['type'] == 'small_airport':
        return [0, 0, 255, 255]
    #Making all other airport dots grey
    else:
        return [150, 150, 150, 160]

def main():
    open_airports_df, closed_airports_df, small_airports_df, medium_airports_df, large_airports_df, heliports_df, seaports_df, balloonports_df, num_airport_types = identify_data(FILENAME)

    num_closed = num_airport_types.get('closed', 0)
    sum_all_ports = len(open_airports_df) + len(closed_airports_df)

    st.title("Global Airport Statistics📊")
    st.divider()
    st.header("Airports By The Numbers:🔢")
    st.text(f"There are {sum_all_ports:,} airports around the world!\n (However, {num_closed:,} are closed)")
    #Below code renames airports to a more presentable looking name
    type_renamed = {
        'heliport': 'Heliports',
        'small_airport': 'Small Airports',
        'medium_airport': 'Medium Airports',
        'large_airport': 'Large Airports',
        'seaplane_base': 'Seaports / Seaplane Bases',
        'balloonport': 'Balloonports',
        'closed': 'Closed Airports'
    }
    renamed_airport_types = num_airport_types.rename(index=type_renamed)
    st.subheader(f"Type Breakdown ({open_airports_df['type'].nunique() + 1} unique types)") #Adding one to account for closed airports
    st.dataframe(renamed_airport_types)
    st.text("Note that every airport besides the 'Closed' category counts towards the number of open airports.")

    st.markdown("##### Visual Breakdown of Airport Types Worldwide ") #[CHART2]
    chart_data = renamed_airport_types.sort_values(ascending=False).reset_index() #[SORT]
    chart_data.columns = ['Airport Type', 'Count']
    #Below code creates a pie chart to show the percentage of types of airports around the world
    fig, ax = plt.subplots(figsize=(10, 10))
    ax.pie(chart_data['Count'],
        autopct='%1.1f%%',
        startangle=90,
        pctdistance=1.1)
    ax.legend(chart_data['Airport Type'],
        title="Airport Types",
        loc="center left",
        bbox_to_anchor=(1, 1))
    ax.axis('equal') #Setting equal so the pie chart comes out as a circle
    st.pyplot(fig) #[CHART1]
    #Below code creates a dictionary to use if functions on later
    map_options = {"All Open Airports": open_airports_df,
               "All Closed Airports": closed_airports_df,
               "All Small Airports": small_airports_df,
               "All Medium Airports": medium_airports_df,
               "All Large Airports": large_airports_df,
               "All Heliports": heliports_df,
               "All Seaports": seaports_df,
               "All Balloonports": balloonports_df}
    see_map = st.selectbox("Select Which Airports To See On A Map", map_options) #[ST1]
    open_airports_df['color'] = open_airports_df.apply(get_color, axis=1)
    if see_map == "All Open Airports": #[MAP]
        st.text("Every Open Airport Location")
        #Using a pydeck map to create an engaging map
        #USED PYDECK website, specifically "Globe View" & "Scatterplot Layer" code & Github to understand what that code means and how to build on it
        layer = pdk.Layer(
            "ScatterplotLayer",
            open_airports_df,
            get_position=['longitude', 'latitude'],
            get_color='color',  #Referring to the colors created earlier
            get_radius='size',
            radius_scale=500,
            pickable=True,
            auto_highlight=True,)
        #Below code sets where the viewer map starts looking at, unnecessary but included it to not mess anything up
        view_state = pdk.ViewState(
            latitude=40.0,
            longitude=-100.0,
            zoom=2,
            pitch=0,)
        #Creating map/chart, found map styles to use and tooltip to set to through Pydeck website
        st.pydeck_chart(pdk.Deck(
            map_style= 'light',
            initial_view_state=view_state,
            layers=[layer],
            tooltip={"html": "<b>{name}</b><br>Type: {type}<br>Country: {iso_country}",
                "style": { "backgroundColor": "steelblue", "color": "white"}}))

    elif see_map == "All Closed Airports": #[MAP]
        st.text("Every Closed Airport Location")
        st.map(closed_airports_df) #Only displaying closed airports
    elif see_map == "All Small Airports": #[MAP]
        st.text("Every Small Airport Location")
        st.map(small_airports_df) #Only displaying small airports
    elif see_map == "All Medium Airports": #[MAP]
        st.text('Every Medium Airport Location')
        st.map(medium_airports_df) #Only displaying medium airports
    elif see_map == "All Large Airports": #[MAP]
        st.text('Every Large Airport Location')
        st.map(large_airports_df) #Only displaying large airports
    elif see_map == "All Heliports": #[MAP]
        st.text("Every Heliport Location")
        st.map(heliports_df) #Only displaying heliports
    elif see_map == "All Seaports": #[MAP]
        st.text("Every Seaport Location")
        st.map(seaports_df) #Only displaying seaports/seabases
    elif see_map == "All Balloonports": #[MAP]
        st.text("Every Balloonport Location")
        st.map(balloonports_df) #Only displaying balloonports

if __name__ == '__main__':
    main()

