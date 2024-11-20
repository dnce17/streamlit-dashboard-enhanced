import streamlit as st
import pandas as pd

st.header("2024 AHI 507 Streamlit Example - Student Modification")
st.subheader("We are going to go through a couple different examples of loading and visualization information into this dashboard")

st.text("""In this streamlit dashboard, we are going to focus on some recently released school learning modalities data from the NCES, for the years of 2021.""")

## https://healthdata.gov/National/School-Learning-Modalities-2020-2021/a8v3-a3m3/about_data
df = pd.read_csv("https://healthdata.gov/resource/a8v3-a3m3.csv?$limit=25000") ## first 1k 

## data cleaning 
df['week_recoded'] = pd.to_datetime(df['week'])
df['week_recoded'] = [date.strftime("%Y-%m-%d") for date in df['week_recoded']]
df['zip_code'] = df['zip_code'].astype(str)

df['week_recoded'].value_counts()

## box to show how many rows and columns of data we have: 
col1, col2, col3 = st.columns(3)
col1.metric("Columns", df.shape[1]) 
col2.metric("Rows", len(df))
col3.metric("Number of unique districts/schools:", df['district_name'].nunique())

## exposing first 1k of NCES 20-21 data
st.dataframe(df)

## toggle learning_modality --> in case user wants to focus on 1 specific chart
st.subheader("Toggle to hide or show week and learning modality charts")
hybrid = st.checkbox("Hybrid", value=True)
in_person = st.checkbox("In Person", value=True)
remote = st.checkbox("Remote", value=True)

## slider
st.subheader("Filter Date Range")
str_dates = [date for date in df['week_recoded'].unique()]
date_selector = st.select_slider(
    'Date Range',
    options=str_dates,
    value=str_dates[-1],
)
st.write(f'**Date Range**: {str_dates[0]} to {date_selector}')

filtered_range = df[pd.to_datetime(df['week_recoded']) <= date_selector]

# DON'T add this or else it will show other unrelated time/date b/w the dates you want to see
# filtered_range['week_recoded'] = pd.to_datetime(filtered_range['week_recoded'])

table = pd.pivot_table(filtered_range, values='student_count', index=['week_recoded'],
                       columns=['learning_modality'], aggfunc="sum")

table = table.reset_index()
table.columns

def toggle_bar_chart(toggle_on, table, x_label, y_label):
    if toggle_on:
        st.bar_chart(table, x=x_label, y=y_label)

## bar chart by week 
toggle_bar_chart(hybrid, table, "week_recoded", "Hybrid")
toggle_bar_chart(in_person, table, "week_recoded", "In Person")
toggle_bar_chart(remote, table, "week_recoded", "Remote")