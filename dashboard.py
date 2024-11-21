import streamlit as st
import pandas as pd
import plotly.express as px

st.write("**Danny Chen** - [GitHub Repo Link](https://github.com/dnce17/streamlit-dashboard-enhanced)")
st.header("2024 AHI 507 Streamlit Example - Modified")
st.subheader("We are going to go through a couple different examples of loading and visualization information into this dashboard")

st.text("""In this streamlit dashboard, we are going to focus on some recently released school learning modalities data from the NCES, for the years of 2021.""")

# https://healthdata.gov/National/School-Learning-Modalities-2020-2021/a8v3-a3m3/about_data
df = pd.read_csv("https://healthdata.gov/resource/a8v3-a3m3.csv?$limit=50000") ## first 1k 

# Data cleaning 
df['week_recoded'] = pd.to_datetime(df['week'])
# Remove timestamp from the date since it isn't used as it's all 00:00:00
df['week_recoded'] = [date.strftime("%Y-%m-%d") for date in df['week_recoded']]

# Box to show how many rows and columns of data we have: 
col1, col2, col3 = st.columns(3)
col1.metric("Columns", df.shape[1]) 
col2.metric("Rows", len(df))
col3.metric("Number of unique districts/schools:", df['district_name'].nunique())

# Exposing first 1k of NCES 20-21 data
st.dataframe(df)


# ---- HORIZONTAL BAR CHART
st.subheader("Changes in Learning Modality Over Time (Weeks)")

# Toggle learning modality (in case user wants to focus on 1 specific chart)
st.write("**Toggle to hide or show week and learning modality charts**")
hybrid = st.checkbox("Hybrid", value=True)
in_person = st.checkbox("In Person", value=True)
remote = st.checkbox("Remote", value=True)

# Slider to filter date for week and learning modality bar charts
st.write(f"**Filter Date Range of Bar Charts Below**")
str_dates = [date for date in df['week_recoded'].unique()]
date_selector = st.select_slider(
    'Date Range',
    options=str_dates,
    value=str_dates[-1],
)

# Shows the date range that the bar charts are showing
st.write(f'**Date Range**: {str_dates[0]} to {date_selector}')

# Filter the date based on the slider
filtered_range = df[pd.to_datetime(df['week_recoded']) <= date_selector]

# NOTE for future reference: DON'T add this or else it will show time/dates outside the df's dates
# filtered_range['week_recoded'] = pd.to_datetime(filtered_range['week_recoded'])

table = pd.pivot_table(filtered_range, values='student_count', index=['week_recoded'],
                       columns=['learning_modality'], aggfunc="sum")

table = table.reset_index()

# In the Streamlit site, this shows a table with the columns
table.columns

# Show/hide bar charts if modality is checked on/off
def toggle_bar_chart(toggle_on, table, x_label, y_label, horizontal=False):
    if toggle_on:
        if horizontal == False:
            st.bar_chart(table, x=x_label, y=y_label)
        else:
            st.bar_chart(table, x=x_label, y=y_label, horizontal=True)

toggle_bar_chart(hybrid, table, "week_recoded", "Hybrid", True)
toggle_bar_chart(in_person, table, "week_recoded", "In Person", True)
toggle_bar_chart(remote, table, "week_recoded", "Remote", True)


# ---- PIE CHART
st.subheader("**Amount of Operational Schools by Learning Modality**")
modality_total_schools = df.groupby("learning_modality")["operational_schools"].sum().reset_index()

# Create a pie chart using Plotly
pie_fig = px.pie(
    modality_total_schools,
    names="learning_modality",  # Categorical column
    values="operational_schools",  # Numeric column
)

# Show both percent and value in pie chart
pie_fig.update_traces(textinfo="value+percent")

# Display the pie chart in Streamlit
st.plotly_chart(pie_fig)


# ---- CHOROPLETH MAP
st.subheader("**Geographical Distribution of Learning Modality in US**")

state_modality_data = df.groupby(["state", "learning_modality"])["student_count"].sum().reset_index()

# Select widget to choose which learning modality to display
modality = st.selectbox("Select Learning Modality", df["learning_modality"].unique(), index=2)

# Filter data for selected modality
filtered_modality = state_modality_data[state_modality_data["learning_modality"] == modality]

# Create choropleth map
fig = px.choropleth(
    filtered_modality,
    locations="state",  # Column with state codes
    locationmode="USA-states",  # Map mode to match US states
    color="student_count",  # Numerical data to color states
    hover_name="state",  # Display state names on hover
    scope="usa",  # Limit map to the USA
    title=f"{modality} Learning - Geographical Distribution",
    color_continuous_scale="Viridis"  # Customize color scale
)

# Show the map in Streamlit
st.plotly_chart(fig)


# ---- BAR CHART
st.subheader("**Distribution of Operational Schools Across States**")

# Get the total amt of operational schools per state
state_total_schools = df.groupby("state")["operational_schools"].sum().reset_index()

st.write("**NOTE**: Hover over the chart and click the fullscreen button to the top right to see all state labels")
st.bar_chart(state_total_schools, x="state", y="operational_schools")