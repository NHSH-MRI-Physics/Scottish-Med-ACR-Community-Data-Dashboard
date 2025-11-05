import streamlit as st
from streamlit_gsheets import GSheetsConnection
import plotly.express as px
from scipy import stats
import pandas as pd
import requests
import xmltodict
st.set_page_config(initial_sidebar_state='collapsed',page_title="Scottish Medium ACR Community Dashboard")

st.title("Scottish Med ACR Community Data Dashboard")
st.markdown("""
This dashboard presents data collected from scottish centers using a medium ACR phantom and analysed using the [Scottish Medium ACR Phantom QA project](https://github.com/NHSH-MRI-Physics/Scottish-Medium-ACR-Analysis-Framework).

Filters for the data can be found on the sidear (arrow the top left). You can view the raw data via the "View Rawdata" link also in the sidebar.
""")
st.cache_data.clear()
st.cache_resource.clear()
conn = st.connection("gsheets", type=GSheetsConnection,ttl=1)
df = conn.read()
df = df.fillna(value="Not Provided")

XMLurl = "https://raw.githubusercontent.com/NHSH-MRI-Physics/Scottish-Medium-ACR-Analysis-Framework/refs/heads/main/ToleranceTable/ToleranceTable_80mmPeg.xml"
response = requests.get(XMLurl)
ToleranceTable = xmltodict.parse(response.content)['ToleranceTable']['Module']
print(ToleranceTable)

st.sidebar.title('Filters')
ScannerManufacturer = st.sidebar.multiselect('Select Scanner Manufacturer', df['ScannerManufacturer'].unique(), default=df['ScannerManufacturer'].unique())
Institution = st.sidebar.multiselect('Select Institution', df['Institution'].unique(), default=df['Institution'].unique())
ScannerModel = st.sidebar.multiselect('Select Scanner Model', df['ScannerModel'].unique(), default=df['ScannerModel'].unique())
FieldStrength = st.sidebar.multiselect('Select Field Strength', df['FieldStrength'].unique(), default=df['FieldStrength'].unique())
st.sidebar.markdown("**Version:** 1.1 Beta")
#st.sidebar.page_link("pages/Rawdata.py", label="Go to Raw Data")

df = df[(df['ScannerManufacturer'].isin(ScannerManufacturer)) & (df['Institution'].isin(Institution)) & (df['ScannerModel'].isin(ScannerModel))& (df['FieldStrength'].isin(FieldStrength))]
#st.write(df.head())


if df.empty:
    st.warning("No data available for the selected filters.")
    st.stop()

def MakePlot(x,y,title,AxisTitle,module=None,test=None):
    tol_low = None
    tol_high = None
    if module != None and test != None:
        for mod in ToleranceTable:
            if mod['@name'] == module:
                for t in mod['Test']:
                    if t['@name'] == test:
                        if '@Min' in t:
                            tol_low = float(t['@Min'])
                        if '@Max' in t:
                            tol_high = float(t['@Max'])
                        break
    print(tol_low,tol_high)

    filtered_df = df[df[y] != "Not Run"]
    filtered_df[y] = pd.to_numeric(filtered_df[y], errors='coerce')
    filtered_df[x] = pd.to_datetime(filtered_df[x], errors='coerce',dayfirst=True)

    fig = px.scatter(filtered_df, x=x, y=y, title=title,hover_data=["ScannerManufacturer","Institution","ScannerModel","ScannerSerialNumber","Sequence","FieldStrength"])
    fig.update_xaxes(title_text="Scan Date")
    fig.update_yaxes(title_text=AxisTitle)
    avg = filtered_df[y].mean()
    n = filtered_df[y].count()
    std_err = stats.sem(filtered_df[y], nan_policy='omit')
    conf_int = stats.t.interval(0.95, n-1, loc=avg, scale=std_err)
    fig.add_hline(
        y=avg,
        line_dash="dash",
        line_color="red",
        annotation_text=f"Average "+AxisTitle+f": {avg:.2f}",
        annotation_position="top left"
    )

    fig.add_hline(
        y=conf_int[0],
        line_dash="dot",
        line_color="blue",
        annotation_text=f"95% Confidence Interval: {conf_int[0]:.2f}",
        annotation_position="bottom left"
    )
    fig.add_hline(
        y=conf_int[1],
        line_dash="dot",
        line_color="blue",
        annotation_text=f"95% Confidence Interval: {conf_int[1]:.2f}",
        annotation_position="top right"
    )
    return fig

st.subheader("SNR")
st.plotly_chart(MakePlot("DateScanned","SNR","SNR","SNR"))
st.plotly_chart(MakePlot("DateScanned","SNRNormalised","Normalised SNR","Normalised SNR"))

st.divider()
st.subheader("Slice Position")
st.plotly_chart(MakePlot("DateScanned","Slice1PositonError","Slice 1 Position Error","Slice 1 Position Error (mm)"))
st.plotly_chart(MakePlot("DateScanned","Slice11PositionError","Slice 11 Position Error","Slice 11 Position Error (mm)"))

st.divider()
st.subheader("Slice Thickness")
st.plotly_chart(MakePlot("DateScanned","SliceThickness","","Slice Thickness (mm)"))

st.divider()
st.subheader("Uniformity")
st.plotly_chart(MakePlot("DateScanned","Uniformity","","Uniformity (%)","Uniformity","ACRMethod"))

st.divider()
st.subheader("Ghosting")
st.plotly_chart(MakePlot("DateScanned","Ghosting","","Ghosting (%)"))

st.divider()
st.subheader("Geometric Accuracy (MagNET Method)")
option = st.selectbox("Choose horizontal or vertical distances:", ["Horizontal", "Vertical"])
if option == "Horizontal":
    st.plotly_chart(MakePlot("DateScanned","TopHorizontalDistances","Top Horizontal Distance Errors","Top Horizontal Distance Errors (mm)"))
    st.plotly_chart(MakePlot("DateScanned","MiddleHorizontalDistances","Middle Horizontal Distance Errors","Middle Horizontal Distance Errors (mm)"))
    st.plotly_chart(MakePlot("DateScanned","BottomHorizontalDistances","Bottom Horizontal Distance Errors","Bottom Horizontal Distance Errors (mm)"))
if option == "Vertical":
    st.plotly_chart(MakePlot("DateScanned","LeftVerticalDistances","Left Vertical Distance Error","Left Vertical Distance Error (mm)"))
    st.plotly_chart(MakePlot("DateScanned","MiddleVerticalDistances","Middle Vertical Distance Error","Middle Vertical Distance Error (mm)"))
    st.plotly_chart(MakePlot("DateScanned","RightVerticalDistances","Right Vertical Distance Error","Right Vertical Distance Error (mm)"))

st.divider()
st.subheader("Spatial Resolution (Contrast Response)")
option = st.selectbox("Choose a Resolution grid:", ["1.1mm", "1.0mm", "0.9mm", "0.8mm"])
if option == "1.1mm":
    st.plotly_chart(MakePlot("DateScanned","1.1mm holes Horizontal","1.1mm grid Resolution Horizontal","1.1mm grid Resolution (%)"))
    st.plotly_chart(MakePlot("DateScanned","1.1mm holes Vertical","1.1mm grid Resolution Vertical","1.1mm grid Resolution (%)"))
if option == "1.0mm":
    st.plotly_chart(MakePlot("DateScanned","1.0mm holes Horizontal","1.0mm grid Resolution Horizontal","1.0mm grid Resolution (%)"))
    st.plotly_chart(MakePlot("DateScanned","1.0mm holes Vertical","1.0mm grid Resolution Vertical","1.0mm grid Resolution (%)"))
if option == "0.9mm":
    st.plotly_chart(MakePlot("DateScanned","0.9mm holes Horizontal","0.9mm grid Resolution Horizontal","0.9mm grid Resolution (%)"))
    st.plotly_chart(MakePlot("DateScanned","0.9mm holes Vertical","0.9mm grid Resolution Vertical","0.9mm grid Resolution (%)"))
if option == "0.8mm":
    st.plotly_chart(MakePlot("DateScanned","0.8mm holes Horizontal","0.8mm grid Resolution Horizontal","0.8mm grid Resolution (%)"))
    st.plotly_chart(MakePlot("DateScanned","0.8mm holes Vertical","0.8mm grid Resolution Vertical","0.8mm grid Resolution (%)"))
