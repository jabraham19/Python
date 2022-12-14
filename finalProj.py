"""
Class: CS230-2
Name: Julia Abraham
Description: Final Project
I pledge that I have completed the programming assignment independently. 
I have not copied the code from a student or any source.
I have not given my code to any student. 
"""

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import pydeck as pdk

FILENAME = "Skyscrapers_2021.csv"


# read in data
def read_data():
    dfSky = pd.read_csv(FILENAME,
                        header=0,
                        names=["Rank", "Name", "City", "Address", "latitude", "longitude",
                               "Completed", "Height", "Meters", "Feet", "Floors",
                               "Material", "Function", "Link"]).set_index("Rank")
    return dfSky


def plotTop(dfSky):
    num = st.number_input("How many skyscrapers do you want to see? ", min_value=1, max_value=100, value=15)
    top = dfSky.query("Rank <= @num").sort_values('Feet', ascending=True)

    heights = top['Feet']
    names = top['Name']
    d = {'heights': heights, 'names': names}
    df = pd.DataFrame(d)

    fig = px.bar(df, x='names', y='heights',
                 labels=dict(names='Buildings', heights='Height (ft.)'))
    # fig.update_yaxes(tickvals=[500, 750, 1000, 1250, 1500, 1750, 2000, 2250, 2500, 2750])
    fig.update_layout(yaxis=dict(tickvals=[500, 750, 1000, 1250, 1500, 1750, 2000, 2250, 2500, 2750]))
    return fig


def plotCity(dfSky):
    cities = dfSky
    city = st.selectbox('Select a city to see how many floors their tallest buildings have!',
                        ['Dubai', 'New York', 'Shenzhen', 'Hong Kong', 'Chicago', 'Kuala Lumpur',
                         'Moscow', 'Guangzhou', 'Shanghai', 'Wuhan'])
    if city == 'Dubai':
        cities = dfSky.query("City == 'Dubai'")
    if city == 'New York':
        cities = dfSky.query("City == 'New York City'")
    if city == 'Shenzhen':
        cities = dfSky.query("City == 'Shenzhen'")
    if city == 'Hong Kong':
        cities = dfSky.query("City == 'Hong Kong'")
    if city == 'Chicago':
        cities = dfSky.query("City == 'Chicago'")
    if city == 'Kuala Lumpur':
        cities = dfSky.query("City == 'Kuala Lumpur'")
    if city == 'Moscow':
        cities = dfSky.query("City == 'Moscow'")
    if city == 'Guangzhou':
        cities = dfSky.query("City == 'Guangzhou'")
    if city == 'Shanghai':
        cities = dfSky.query("City == 'Shanghai'")
    if city == 'Wuhan':
        cities = dfSky.query("City == 'Wuhan'")

    floors = cities['Floors']
    names = cities['Name']
    d = {'floors': floors, 'names': names}
    df = pd.DataFrame(d)

    fig = px.bar(df, x='names', y='floors',
                 labels=dict(names='Buildings', floors='Number of floors'))
    return fig


def countCities(dfSky):
    cityCount = dfSky['City'].value_counts()
    labels = ['Dubai', 'New York', 'Shenzhen', 'Hong Kong', 'Chicago', 'Kuala Lumpur', 'Moscow',
              'Guangzhou', 'Shanghai', 'Wuhan', 'Busan', 'Guiyang', 'Chongquin', 'Tianjin', 'Changsha',
              'Nanning', 'Beijing', 'Dalian', 'Abu Dhabi', 'Nanjing', 'Wuxi', 'Philadelphia', 'Kunming',
              'Zhenjiang', 'Zhuhai', 'Kaohsiung', 'Los Angeles', 'Seoul', 'Shenyang', 'Kuwait City',
              'Suzhou', 'Ho Chi Minh', 'St. Petersburg', 'Mecca', 'Taipei', 'Jinan']
    fig1, ax1 = plt.subplots()
    ax1.pie(cityCount, labels=labels, shadow=True, autopct='%1.0f%%', startangle=90)
    ax1.axis('equal')

    return fig1


def mapSky(dfSky):
    mapData = dfSky[['latitude', 'longitude']]
    st.pydeck_chart(pdk.Deck(
        map_style=None,
        initial_view_state=pdk.ViewState(
            latitude=25.197197,
            longitude=55.2743764,
            zoom=10,
            pitch=50,
        ),
        layers=[
            pdk.Layer(
                'HexagonLayer',
                data=mapData,
                get_position='[longitude, latitude]',
                radius=300,
                elevation_scale=4,
                elevation_range=[0, 1000],
                pickable=True,
                extruded=True,
            ),
            pdk.Layer(
                'ScatterplotLayer',
                data=mapData,
                get_position='[longitude, latitude]',
                get_color='[200, 30, 0, 160]',
                get_radius=200,
            ),
        ],
    ))

    return mapData


# main function
def main():
    dfSky = read_data()
    page = st.sidebar.selectbox('Select page', ['Tallest Skyscrapers', 'Cities'])

    if page == 'Tallest Skyscrapers':
        st.title("Tallest Skyscrapers")
        # top num dropdown
        # select box for feet vs meters
        chart = plotTop(dfSky)
        st.write(chart)
        chart = plotCity(dfSky)
        st.write(chart)

    elif page == 'Cities':
        st.title("Cities with the Tallest Skyscrapers")
        chart = mapSky(dfSky)
        st.map(chart)
        chart = countCities(dfSky)
        st.pyplot(chart)


if __name__ == "__main__":
    main()
