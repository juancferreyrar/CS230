import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import seaborn as sns
import folium
from streamlit_extras import let_it_rain
import matplotlib.colors as mcolors
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster
import plotly.express as px


#Name: Juan Carlos Ferreyra
#CS230: Section 4
#Data: Motorcycle Vehicle Crashes in MA in 2017
#URL:

#Description:
#This program emphasizes and prioritizes the user interface, to make sure to go with the theme of the data. Firstly, the main page
#serves to introduce and explain the main variables to the user, so that they can get a feel of the main data points. This page includes icons
#and information such as most popular and least popular city crash. The data dictionary section uses a dictionary to create a table and display the raw data,
#for both the user to be curious about exploring the data and understanding their variables. The descriptive data section creates an environment for the user to see
#the main details of the data set. The weather tab is empty until the user inputs their choices, they can chose a type of weather, which will then create
#two visualizations, one based on fatality and one based on type of accident. It also creates a pie chart on the amount of variables the user wants. For time,
#I decided to parse through the time and create a histogram, based on grouping the days on each month, to be able to show visually the months with more accidents. The color intensity is
#also based on the amount of crashes on that day. The user is able to put in a certain date and return the date.
#For the location tab, the user choses one of four columns, where the user decides where to sort the location, for example (the city, town, street).
#It then creates a pie chart based on the cities and compares the number of crashes within the city against other cities. For the map, I created a map using folium, where the labels (based on fatality) got clustered when zooming out, the darker the
#color, the more crashes on the area. A similar graph with Plotly was created, which sorted based on the road condition. The safety tab is what I describe as my "fun" tab, where I experimented
#using streamlit-extras to create a car rain and embedd a youtube video. Finally, I use one more streamlit button to link my linkedin page, for any potential recruiters to see my app.

#Selected Data Path
data = "C:/Users/jcfer/OneDrive - Bentley University/pythonProject/Program5/2017_Crashes.csv"
df = pd.read_csv(data)

#Simplify the usage of creating buttons for graphs by introducing a function: [PY3]
def get_data(column_name): #Function will help for sidebar in streamlit
    return df[column_name].dropna().unique() #[DA1]

#[PY1]
def get_non_unique_data(column_name, include_na =True): #Function will help for extracting repeating values
    if include_na:
        return df[column_name]
    else:
        return df[column_name].dropna()

#Multiple Variable Returning Functions [PY2]
def most_x_function(data_column):  # Gets you the highest count of crash ID on a selected column
    counted = df[data_column].value_counts()
    named_value = counted.idxmax() #Returns the highest ID amount on selected column
    count_value = counted.max()
    return(named_value,count_value)

def least_x_function(data_column):  # Gets you the lowest count of crash ID on selected column (Which is not 0)
    counted = df[data_column].value_counts()
    filtered_counts  = counted[counted > 0] #Checks that the value is not 0
    named_value = counted.idxmin() #Returns the lowest ID amount on selected column
    count_value = counted.min()
    return(named_value,count_value)

#Title of Streamlit
st.title("Motor Vehicle Accidents in Massachusetts in 2017")

#For organization purposes, separated in to tabs
tab1, tab2, tab3 , tab4 , tab5, tab6 , tab7, tab8, tab9= st.tabs(["Main Page","Data Dictionary", "Descriptive Statistics","Weather","Time","Location","Map","Safety","About"]) #[ST1]

#Tab1 Is where we introduce the data set, and use HTMl to give visuals on the main findings on the data set.
with tab1:
    mass_logo = "C:/Users/jcfer/OneDrive - Bentley University/pythonProject/Program5/Seal_of_Massachusetts.svg.png"
    col1, col2 = st.columns(2)
    col1.image(mass_logo, use_column_width=True) #[ST2]

    #Header
    col2.header("2017 Massachusetts Crashes")
    #Description of Data set and exploration
    st.write("This dataset contains crash details for 2017, and includes factors such as number of vehicles involved, total fatal injuries, crash severity, weather condition, and several more attributes that would allow us to visuallize the motor vehicle accidents.")

    #Uses the function get_data to be able to find certan metrics, in this case number of crashes.
    total_crashes = get_data("OBJECTID")
    amount_total_crashes = len(total_crashes)

    #Measures a more complex variable, in this case the amount of fatal vs non-fatal crashes
    all_severity_data = get_non_unique_data("CRASH_SEVERITY_DESCR", include_na=False) #Drops Null values
    fatal_injury_count = (all_severity_data == "Fatal injury").sum()
    non_fatal_injury_count = (all_severity_data == "Non-fatal injury").sum()

    #Date Counts, calling previously defined functions
    date_value, date_count = most_x_function("CRASH_DATE_TEXT")
    min_date_value, min_date_count = least_x_function("CRASH_DATE_TEXT")
    max_city_value, max_city_count = most_x_function("CITY")
    min_city_value, min_city_count = least_x_function("CITY")

    #Utilizing HTML and CSS as external feature for aesthetic [ST3]
    #This is a part of my code that took me a long time, as I wanted to display an aesthetic that would match the theme, so, learning about fonts, classes, color, and other features to maintain it consistent was a lot of trail and error.
    st.markdown(f"""
        <style>
            .big-font {{
                font-size:40px !important;
            }}
            .number {{
                display: inline-block;
                margin-right: 300px;
            }}
        </style>
        <p class="big-font">Total Amount of Crashes in Data: {amount_total_crashes}</p>
        <p>Shortened data set for purpose of project simplicity, hence we account for 10,000 crashes</p>
        <p class="big-font" style="color: red;"> Non-Fatal VS Fatal Crashes</p>
        <p>Count of each category, fatal crashes only represents around 10% of crashes</p>
        <p class="big-font">
            <span class="number">{non_fatal_injury_count}</span>
            <span>{fatal_injury_count}</span>
        </p>
        <h1>The Most and Least Popular Days to Crash</h1>
        """,unsafe_allow_html=True)

    #Wanted to ensure usage of Streamlit features, such as streamlit Image to follow program requirement.
    #[DA3] Several through the HTMl
    st.image("C:/Users/jcfer/OneDrive - Bentley University/pythonProject/Program5/calendar.png",width=100)
    st.markdown(f"""
        <p class="big-font">Most Popular Day to Crash: {date_value}</p>
        <p> After counting the number of crashes in each day, the most popular day to crash was on the 9th of December, 2017. </p>
        <p class="number"> Amount of crashes on that day: {date_count} </p>
         <p class="big-font">Least Popular Day to Crash: {min_date_value}</p> 
        <p> After counting the number of crashes in each day, the least popular day to crash was on the 27th of February, 2017.</p>
        <p class="number"> Amount of crashes on that day: {min_date_count} </p>
        <br>
        <h1>The Most and Least Popular Cities where Crashes Occur</h1>
        """,unsafe_allow_html=True)
    st.image("C:/Users/jcfer/OneDrive - Bentley University/pythonProject/Program5/Ma_towns.png",width=500) #[ST4]
    st.markdown(f"""
        <p class="big-font">Most Popular City to Crash: {max_city_value.title()}</p>
        <p> The amount of crashes in the town where: {max_city_count}</p>
        <p class="big-font">Most Popular City to Crash: {min_city_value.title()}</p>
        <p> The amount of crashes in the town where: {min_city_count}</p>
        
        """,unsafe_allow_html=True)

    #CHECK IF THERE IS A SWITCH TAB FUNCTION WITH STREAMLIT
#Simplifying the data set by associating it to a dictionary, imported from the original data set
with tab2:
    st.header("Data Dictionary")
    st.write("This section is meant as a tool for the programmer to be able to better understand the data in the data cleansing phase, and to also be transparent with the variables provided in the data set.")
    st.image("C:/Users/jcfer/OneDrive - Bentley University/pythonProject/Program5/Dictionary.png",width=100, caption="Dictionary")
    data_dictionary = {'Crash Number': 'CRASH_NUMB',
        'City Town Name': 'CITY_TOWN_NAME',
        'Crash Date Text': 'CRASH_DATE_TEXT',
        'Crash Time': 'CRASH_TIME',
        'Crash Date-Time Accurate When Exported': 'CRASH_DATETIME',
        'Crash Hour': 'CRASH_HOUR',
        'Crash Status': 'CRASH_STATUS',
        'Crash Severity': 'CRASH_SEVERITY_DESCR',
        'Max Injury Severity Reported': 'MAX_INJR_SVRTY_CL',
        'Number of Vehicles': 'NUMB_VEHC',
        'Total NonFatal Injuries': 'NUMB_NONFATAL_INJR',
        'Total Fatal Injuries': 'NUMB_FATAL_INJR',
        'Police Agency Type': 'POLC_AGNCY_TYPE_DESCR',
        'Manner of Collision': 'MANR_COLL_DESCR',
        'Vehicle Actions Prior to Crash (All Vehicles)': 'VEHC_MNVR_ACTN_CL',
        'Vehicle Travel Direction (All Vehicles)': 'VEHC_TRVL_DIRC_CL',
        'Vehicle Sequence of Events (All Vehicles)': 'VEHC_SEQ_EVENTS_CL',
        'Light Condition': 'AMBNT_LIGHT_DESCR',
        'Weather Condition': 'WEATH_COND_DESCR',
        'Road Surface Condition': 'ROAD_SURF_COND_DESCR',
        'First Harmful Event': 'FIRST_HRMF_EVENT_DESCR',
        'Most Harmful Event (All Vehicles)': 'MOST_HRMFL_EVT_CL',
        'Driver Contributing Circumstances (All Drivers)': 'DRVR_CNTRB_CIRC_CL',
        'Vehicle Configuration (All Vehicles)': 'VEHC_CONFIG_CL',
        'Street Number': 'STREET_NUMB',
        'Roadway': 'RDWY',
        'Distance and Direction from Intersection': 'DIST_DIRC_FROM_INT',
        'Near Intersection Roadway': 'NEAR_INT_RDWY',
        'Milemarker Route': 'MM_RTE',
        'Distance and Direction from Milemarker': 'DIST_DIRC_MILEMARKER',
        'Milemarker': 'MILEMARKER',
        'Exit Route': 'EXIT_RTE',
        'Distance and Direction from Exit': 'DIST_DIRC_EXIT',
        'Exit Number': 'EXIT_NUMB',
        'Distance and Direction from Landmark': 'DIST_DIRC_LANDMARK',
        'Landmark': 'LANDMARK',
        'Roadway Junction Type': 'RDWY_JNCT_TYPE_DESCR',
        'Traffic Control Device Type': 'TRAF_CNTRL_DEVC_TYPE_DESCR',
        'Trafficway Description': 'TRAFY_DESCR_DESCR',
        'Jurisdiction-linked RD': 'JURISDICTN',
        'First Harmful Event Location': 'FIRST_HRMF_EVENT_LOC_DESCR',
        'Non-Motorist Type (All Persons)': 'NON_MTRST_TYPE_CL',
        'Non-Motorist Action (All Persons)': 'NON_MTRST_ACTN_CL',
        'Non-Motorist Location (All Persons)': 'NON_MTRST_LOC_CL',
        'Is Geocoded': 'IS_GEOCODED',
        'Geocoding Method': 'GEOCODING_METHOD_NAME',
        'X': 'X',
        'Y': 'Y',
        'Latitude': 'LAT',
        'Longitude': 'LON',
        'Document IDs': 'RMV_DOC_IDS',
        'Crash Report IDs': 'CRASH_RPT_IDS',
        'Year': 'YEAR',
        'Age of Driver - Youngest Known': 'AGE_DRVR_YNGST',
        'Age of Driver - Oldest Known': 'AGE_DRVR_OLDEST',
        'Age of Non-Motorist - Youngest Known': 'AGE_NONMTRST_YNGST',
        'Age of Non-Motorist - Oldest Known': 'AGE_NONMTRST_OLDEST',
        'Driver Distracted By (All Drivers)': 'DRVR_DISTRACTED_CL',
        'District': 'DISTRICT_NUM',
        'RPA': 'RPA_ABBR',
        'Vehicle Emergency Use (All Vehicles)': 'VEHC_EMER_USE_CL',
        'Vehicle Towed From Scene (All Vehicles)': 'VEHC_TOWED_FROM_SCENE_CL',
        'County Name': 'CNTY_NAME',
        'FMCSA Reportable (All Vehicles)': 'FMCSA_RPTBL_CL',
        'FMCSA Reportable (Crash)': 'FMCSA_RPTBL',
        'Hit and Run': 'HIT_RUN_DESCR',
        'Locality': 'LCLTY_NAME',
        'Road Contributing Circumstance': 'ROAD_CNTRB_DESCR',
        'School Bus Related': 'SCHL_BUS_RELD_DESCR',
        'Speed Limit': 'SPEED_LIMIT',
        'Traffic Control Device Functioning': 'TRAF_CNTRL_DEVC_FUNC_DESCR',
        'Work Zone Related': 'WORK_ZONE_RELD_DESCR',
        'AADT-linked RD': 'AADT',
        'AADT Year-linked RD': 'AADT_YEAR',
        'Peak % Single Unit Trucks-linked RD': 'PK_PCT_SUT',
        'Average Daily % Single Unit Trucks-linked RD': 'AV_PCT_SUT',
        'Peak % Combo Trucks-linked RD': 'PK_PCT_CT',
        'Average Daily % Combo Trucks-linked RD': 'AV_PCT_CT',
        'Curb-linked RD': 'CURB',
        'Truck Route-linked RD': 'TRUCK_RTE',
        'Left Sidewalk Width-linked RD': 'LT_SIDEWLK',
        'Right Sidewalk Width-linked RD': 'RT_SIDEWLK',
        'Left Shoulder Width-linked RD': 'SHLDR_LT_W',
        'Left Shoulder Type-linked RD': 'SHLDR_LT_T',
        'Surface Width-linked RD': 'SURFACE_WD',
        'Surface Type-linked RD': 'SURFACE_TP',
        'Right Shoulder Width-linked RD': 'SHLDR_RT_W',
        'Right Shoulder Type-linked RD': 'SHLDR_RT_T',
        'Number of Travel Lanes-linked RD': 'NUM_LANES',
        'Number of Opposing Travel Lanes-linked RD': 'OPP_LANES',
        'Median Width-linked RD': 'MED_WIDTH',
        'Median Type-linked RD': 'MED_TYPE',
        'Urban Type-linked RD': 'URBAN_TYPE',
        'Functional Classification-linked RD': 'F_CLASS',
        'Urbanized Area-linked RD': 'URBAN_AREA',
        'Federal Aid Route Number-linked RD': 'FD_AID_RTE',
        'Facility Type-linked RD': 'FACILITY',
        'Street Operation-linked RD': 'OPERATION',
        'Access Control-linked RD': 'CONTROL',
        'Number of Peak Hour Lanes-linked RD': 'PEAK_LANE',
        'Speed Limit-linked RD': 'SPEED_LIM',
        'Street Name-linked RD': 'STREETNAME',
        'From Street Name-linked RD': 'FROMSTREETNAME',
        'To Street Name-linked RD': 'TOSTREETNAME',
        'City-linked RD': 'CITY',
        'Structural Condition-linked RD': 'STRUCT_CND',
        'Terrain-linked RD': 'TERRAIN',
        'Urban Location Type-linked RD': 'URBAN_LOC_TYPE',
        'Opposing Direction Speed Limit-linked RD': 'OP_DIR_SL',
        'Undivided Left Shoulder Type-linked RD': 'SHLDR_UL_T',
        'Undivided Left Shoulder Width-linked RD': 'SHLDR_UL_W',
        'Federal Functional Classification-linked RD': 'F_F_CLASS'
    }
    df_dictionary = pd.DataFrame(list(data_dictionary.items()), columns=['Description', 'Column Name']) #[PY5]

    # Display the DataFrame as a table in Streamlit
    st.table(df_dictionary) #Created a Table [ST5]

    st.header("Raw Data")
    st.dataframe(df)

with tab3:
    st.header("Descriptive Statistics of Data")
    st.image("C:/Users/jcfer/OneDrive - Bentley University/pythonProject/Program5/Calculator.png",width=100)
    st.write("The non-categorical, or in other words the numerical data from the data set. Keep in mind these are not ALL numerical values, but rather the once which made sense running a statistical analysis on. OBJECTID, or the ID of the Car Crash would not provide a meaningful average or max, since the numbers are not meant to be used in calculations.")
    #This section took a lot of manual effort, because deciding which variables where significant or not required meticulous data cleansing as it reminded me of the importance of understanding your data before you go in to a program.
    columns_of_interest = ["CRASH_NUMB", "NUMB_VEHC", "NUMB_NONFATAL_INJR", "NUMB_FATAL_INJR", "SPEED_LIMIT"]
    description = df[columns_of_interest].describe() #[PY4]
    st.write(description)

    city_crash_counts = df["CITY"].value_counts().sort_values(ascending=False)
    st.write("Cities with the most crashes:")
    st.table(city_crash_counts.head(5)) #[DA2]
with tab4:
    weather_conditions = get_data('ROAD_SURF_COND_DESCR')
    #Calls the function to obtain the names for the sidebar selectbox
    st.sidebar.header("Weather Condition Selector")
    st.sidebar.write("To use this section, go to the weather tab!")
    selected_weather = st.sidebar.selectbox("Choose a weather condition:", weather_conditions) #[ST6]
    #[ST7]
    top_n = st.sidebar.number_input("How many weather conditions do you want to see in the Pie Chart? The rest will be grouped in 'Other'.",min_value=1, max_value=len(weather_conditions), value=5, step=1)
    st.sidebar.write("Remember to stay in the range from 1 to", len(weather_conditions)) #Interactive based on Variable
    submit_weather = st.sidebar.button("Submit Weather")

    #If submitted button is pressed, this logic took me a while to implement because whenever I would try to click on an option, the sidebar would dissappear.
    if submit_weather and selected_weather:
        st.write("This section will display visualization based on your response, we are trying to visually show the effect of weather on the crashes!")
        st.sidebar.write("You selected:", selected_weather) #Small details for aesthetic

        #This was one of the first graphs, so I really wanted to pay attention to detail and make sure that the titles change.
        st.header(f"Data Filtered Based on a {selected_weather} Day")

        # Filter data based on selected weather condition
        filtered_data = df[df["ROAD_SURF_COND_DESCR"] == selected_weather] #[DA4]
        # Plotting Crash Severity
        #[V1] and [V2], Bar Graphs with Manner of Collition and Crash Severity Considered.
        plt.figure(figsize=(10, 6))
        #Creating a graph in Seaborn
        sns.countplot(data=filtered_data, x="CRASH_SEVERITY_DESCR",
                      order=filtered_data["CRASH_SEVERITY_DESCR"].value_counts().index, color='gray')
        plt.xlabel("Crash Severity")
        plt.ylabel("Number of Crashes")
        plt.title(f'Count of Crash IDs by Severity for {selected_weather} Conditions')
        #Because of nature of crash severity description, rotating would be more aesthetic
        plt.xticks(rotation=45)
        plt.tight_layout()

        st.pyplot(plt)

        # Plotting Manner of Collision
        plt.figure(figsize=(10, 6))
        sns.countplot(data=filtered_data, x="MANR_COLL_DESCR",
                      order=filtered_data["MANR_COLL_DESCR"].value_counts().index, color='gray')
        plt.xlabel("Manner of Collision")
        plt.ylabel("Number of Crashes")
        plt.title(f'Count of Crash IDs by Crash Condition for {selected_weather} Conditions')
        plt.xticks(rotation=45)
        plt.tight_layout()
        st.pyplot(plt)

        # Preparing data for the pie chart [V3]
        weather_counts = df["ROAD_SURF_COND_DESCR"].value_counts()
        if len(weather_counts) > top_n:
            top_weather = weather_counts[:top_n]
            other_weather = pd.Series(weather_counts[top_n:].sum(), index=["Other"])
            final_weather_counts = pd.concat([top_weather, other_weather])
        else:
            final_weather_counts = weather_counts

        #Very important line of code for madplotlib, as theme is not the happiest.
        colors = plt.cm.Greys(np.linspace(0.2, 0.7, len(final_weather_counts)))

        # Displaying the pie chart
        plt.figure(figsize=(10, 7))
        if top_n > 4:
            wedges, texts, autotexts = plt.pie(final_weather_counts, autopct='%1.1f%%', startangle=140, colors=colors)
            plt.legend(wedges, final_weather_counts.index, title="Weather Conditions", loc="center left",bbox_to_anchor=(1, 0, 0.5, 1))
        else:
            plt.pie(final_weather_counts, labels=final_weather_counts.index, autopct='%1.1f%%', startangle=140,colors=colors)
        plt.title(f"Distribution of Weather Conditions Leading to Crashes in Top {top_n} Conditions")
        st.pyplot(plt)
    else:
        st.sidebar.write("Select a condition and press submit.")
with tab5:
    df["CRASH_DATE_TEXT"] = pd.to_datetime(df["CRASH_DATE_TEXT"], format='%m/%d/%Y')
    df["DATE"] = df["CRASH_DATE_TEXT"].dt.date
    daily_crashes = df.groupby('DATE')['CRASH_NUMB'].count()#[DA7]
    max_crashes = daily_crashes.max()
    min_crashes = daily_crashes.min()

    norm = mcolors.Normalize(vmin=min_crashes, vmax=max_crashes, clip=True)
    mapper = plt.cm.ScalarMappable(norm=norm, cmap=plt.cm.Greys) #Again the imporance of color

    st.title("Crash Data Visualization")
    st.write("This chart represents the number of crashes per day, scaled by color intensity.")

    fig, ax = plt.subplots()
    bars = ax.barh(daily_crashes.index, daily_crashes.values, color=[mapper.to_rgba(x) for x in daily_crashes.values]) #[PY4]
    ax.set_xlabel("Number of Crashes")
    ax.set_ylabel("Date")
    ax.set_title("Daily Crashes Visualized by Color Intensity")

    st.pyplot(fig)
    #[V4]

    min_date = min(df["DATE"])
    max_date = max(df["DATE"])

    user_date = st.date_input( #[ST8]
        "Choose a date to see the number of crashes:",
        value=min_date,
        min_value=min_date,
        max_value=max_date
    )

    if st.button("Show Number of Crashes"):
        if user_date in daily_crashes.index:
            st.write(f"The number of crashes on {user_date} was {daily_crashes[user_date]}")
        else:
            st.write("No crashes recorded on this date.")
with tab6:
    st.header("Location Selector Analysis")
    location_selector = ["Sort by City", "Sort by Roadway", "Sort by Street", "Sort by County"]
    st.sidebar.header("Location Condition Selector")
    st.sidebar.write("To use this section, go to the location tab!")

    chosen_location = st.sidebar.selectbox("Lets sort by location, but what metric will you chose?",location_selector)
    selected_column = {
        "Sort by City": "CITY",
        "Sort by Roadway": "RDWY",
        "Sort by Street": "STREETNAME",
        "Sort by County": "CNTY_NAME"
    }.get(chosen_location, "CITY") #[PY5]


    filtered_location = get_data(selected_column)
    #Using the multiselect values, a pie chart is created [V5] [DA5]
    selected_values = st.multiselect("Select locations:", filtered_location)

    submit_location = st.button("Submit Location")

    if submit_location and selected_values:
        filtered_df = df[df[selected_column].isin(selected_values)]
        total_selected_crashes = filtered_df["CRASH_NUMB"].sum()
        total_crashes = df["CRASH_NUMB"].sum()

        data = [total_selected_crashes, total_crashes - total_selected_crashes] #[DA9]
        labels = ["Selected Locations", "Other Locations"]
        #Again, usage of color was important for themes. This line of code took me research to learn about the different predetermined themes
        colors = plt.cm.Greys(np.linspace(0.2,0.7,len(data)))
        fig, ax =plt.subplots()
        ax.pie(data, labels=labels, autopct='%1.1f%%', startangle=90, colors=colors)
        ax.axis('equal')
        st.pyplot(fig)



with tab7:
    st.header("Map of Crashes with Folium")
    st.write("This map visualizes the locations of motor vehicle accidents using Folium Library.")
    #Creating a map with Folium [V6]-External Library-Foliun abd MarkerCluster
    # Set the initial location and zoom level
    m = folium.Map(location=[42.4072, -71.3824], zoom_start=8)

    # Initialize a marker cluster
    marker_cluster = MarkerCluster().add_to(m)

    # Efficiently process data and add to the map using clusters
    for idx, row in df.iterrows(): #[DA8]
        if pd.notna(row['LAT']) and pd.notna(row['LON']):
            folium.Marker(
                location=[row['LAT'], row['LON']],
                popup=f"Crash Severity: {row['CRASH_SEVERITY_DESCR']}",
                icon=folium.Icon(color="red")
            ).add_to(marker_cluster)

    # Render the map with the marker cluster
    folium_static(m)

    #Used this for folium maps https://www.kaggle.com/code/lucaspcarlini/clustering-and-visualisation-using-folium-maps

    #Map with Plotly [V7] External library-plotly.express
    #https://plotly.com/python/mapbox-layers/
    st.header("Map of Crashes with Plotly")
    st.write("This map visualizes the locations of motor vehicle accidents using Plotly Library.")

    # Filter data to remove any rows with missing coordinates
    map_data = df.dropna(subset=['LAT', 'LON'])

    # Create a scatter plot on the map
    fig = px.scatter_geo(map_data,
                         lat='LAT',
                         lon='LON',
                         color="ROAD_SURF_COND_DESCR",
                         hover_name="ROAD_SURF_COND_DESCR",
                         size_max=15,
                         title="Motor Vehicle Accidents Visualization",
                         template="plotly_dark")

    # Adjust map layout for zoom
    fig.update_geos(
        visible=True,
        # Increase the scale value to zoom in
        projection=dict(scale=80),
        center=dict(lat=42.4072, lon=-71.3824),
    )
    fig.update_layout(height=600)

    st.plotly_chart(fig, use_container_width=True)
with tab8:
    st.header("Safety Disclaimer!")
    st.write("As we have seen, the weather, time of day and location are all factors that we must consider when driving, and while this data set includes several incidents, it only accounts for a year worth of motor vehicle accidents.")
    st.header("Please be carefull when driving!")
    st.write("The following video is published by Smart Drive Test, to promote safe driving!")
    #[ST9]
    st.video("https://www.youtube.com/watch?v=K11S1S4C1qA&ab_channel=SmartDriveTest")
    let_it_rain.rain( #External Library-streamlit_extras
        emoji="🚗",
        font_size=30,
        falling_speed=5,
        animation_length="infinite",
    )
#To call the let_it_rain function, I got inspiration off of https://www.youtube.com/watch?v=RRXFXEzjOWo&ab_channel=CodingIsFun
with tab9:
    st.header("About Me")
    headshot = "C:/Users/jcfer/OneDrive - Bentley University/pythonProject/Program5/CoverPhoto.jpg"
    col1, col2 = st.columns(2)
    col1.image(headshot, use_column_width=True)
    col2.write("My name is Juan Carlos Ferreyra, and I am currently a second-year student at Bentley University pursuing a double degree in Data Analytics and Computer Information Systems, while also pursuing a minor in Sociology. My determination for problem-solving and collaborating has led me to become a tutor for both the CIS Sandbox and the Undergraduate Academic Service, where I am able to practice learned concepts by helping diligent students succeed. I'm currently working to further develop my skills in Java, SQL, Excel, R-Studio, Tableau, and Python to be able to effectively use these skills in the workforce. I am a determined student looking to work for Summer 2024 in an analytics-oriented role to gain experience in the field I am passionate about.")
    st.write("Any Questions? Please feel free to connect with me on Linkedin.")
    #[ST10]
    st.link_button("Linkedin", "https://www.linkedin.com/in/juancarlosferreyra/")





