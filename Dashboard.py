import streamlit as st
from streamlit_gsheets import GSheetsConnection
import plotly.express as px

conn = st.connection("gsheets", type=GSheetsConnection)
df = conn.read()

st.write(df.head())
#fig = px.scatter(df, x=df.columns[0], y=df.columns[1], title="Scatter Plot")
#st.plotly_chart(fig)