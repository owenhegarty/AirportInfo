import streamlit as st
import pandas as pd

from Global_Statistics import main as page2_main
from Airport_Finder import main as page3_main
from Recordholders import main as page4_main

FILENAME = "airport-codes.csv" #Setting symbolic constant

def home_page_content():
    df = pd.read_csv(FILENAME)
    #Page display code
    st.title("Home Page🏡")
    st.divider()
    st.header("Worldwide Airport Directory🛫")
    st.text("This website is a hub for all the information about airports across the world!")
    st.text("Use the navigation sidebar on the left to explore the data on global airports.")

    st.subheader("✈️ Global Airport Fun Facts")
    #Below code filters through iata codes to find major airports
    major_hubs_with_iata = [airport for airport in df.to_dict('records') if pd.notna(airport.get('iata_code'))] #[LISTCOMP] #[DICTMETHOD]

    st.info(f"""**Fact 1:**
    Out of the {len(df):,} airfields in the world, only **{len(major_hubs_with_iata):,}** are major travel hubs, as they have a 3-letter IATA code like 'JFK' or 'LHR'.""")
    #Below code filters through dictionary to find airports above 5k altitude
    high_altitude_airports = [airport for airport in df.to_dict('records') if pd.notna(airport.get('elevation_ft')) and airport.get('elevation_ft') > 5000 and airport.get('type') != 'closed'] #[LISTCOMP] #[FILTER2] #[DICTMETHOD]

    st.info(f"""**Fact 2:**
    There are **{len(high_altitude_airports):,}** airports built more than **5,000 feet** above sea level. The 'Recordholders' page shows the highest one!""")
    #Below code filters through dictionary to find number of seaport bases
    seaports_list = [airport['name'] for airport in df.to_dict('records') if airport.get('type') == 'seaplane_base'] #[LISTCOMP]

    st.info(f"""**Fact 3:**
    This directory includes **{len(seaports_list):,}** Seaplane Bases.""")

    st.divider()
    st.text("Explore the data on the other pages to see maps, search specific airports, and find global recordholders!")

def main():
    st.sidebar.title("✈️ Airport Directory Navigation") #Creating a sidebar to connect all pages

    pages = {
        "Home Page": home_page_content,
        "Global Statistics": page2_main,
        "Airport Finder": page3_main,
        "Recordholders": page4_main
    }

    selection = st.sidebar.selectbox("Go to", list(pages.keys())) #[ST3]
    #Above and below code assigns pages into the sidebar
    page_function = pages[selection]
    page_function()

if __name__ == '__main__':
    main()




