import streamlit as st
from streamlit_gsheets import GSheetsConnection
import plotly.express as px
from scipy import stats
import pandas as pd

st.title("Scottish Med ACR Community Data Dashboard")
st.markdown("""
This page has the raw data used in the plots on the homepage.
""")
conn = st.connection("gsheets", type=GSheetsConnection)
df = conn.read()


st.sidebar.title('Filters')
ScannerManufacturer = st.sidebar.multiselect('Select Scanner Manufacturer', df['ScannerManufacturer'].unique(), default=df['ScannerManufacturer'].unique())
Institution = st.sidebar.multiselect('Select Institution', df['Institution'].unique(), default=df['Institution'].unique())
ScannerModel = st.sidebar.multiselect('Select Scanner Model', df['ScannerModel'].unique(), default=df['ScannerModel'].unique())
FieldStrength = st.sidebar.multiselect('Select Field Strength', df['FieldStrength'].unique(), default=df['FieldStrength'].unique())
#st.sidebar.page_link("Dashboard.py", label="Go to Dashboard")

df = df[(df['ScannerManufacturer'].isin(ScannerManufacturer)) & (df['Institution'].isin(Institution)) & (df['ScannerModel'].isin(ScannerModel))]


if df.empty:
    st.warning("No data available for the selected filters.")
    st.stop()

st.write(df)