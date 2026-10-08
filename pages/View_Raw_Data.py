import streamlit as st
from streamlit_gsheets import GSheetsConnection
import plotly.express as px
from scipy import stats
import pandas as pd

st.title("Scottish Medium ACR Community Data Dashboard")

from PasswordChecking import check_password
if not check_password():
    st.stop()

if 'HighlightedStudies' not in st.session_state:
    st.session_state['HighlightedStudies'] = []

if 'HighlightedStudies_rows' not in st.session_state:
    st.session_state['HighlightedStudies_rows'] = []
    
st.markdown("""
This page has the raw data used in the plots on the homepage. If you select a row in the table below it will be highlighted in the plots on the homepage, you can select multiple rows.
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

#st.write(df)

event = st.dataframe(
    df,
    use_container_width=True,
    hide_index=True,
    on_select="rerun",
    selection_mode="multi-row",
    key="highlighted_df_widget",
    selection_default={"selection": {"rows": st.session_state['HighlightedStudies_rows']}}
)


if event.selection and "rows" in event.selection:
    st.session_state['HighlightedStudies_rows'] = event.selection["rows"]
    st.session_state['HighlightedStudies'] = df.iloc[event.selection.rows]
    
#print( st.session_state['HighlightedStudies_rows'])
#print(df.iloc[event.selection.rows])
#st.session_state['HighlightedStudies'] = df.iloc[event.selection.rows]
#print(st.session_state['HighlightedStudies'].index.tolist())