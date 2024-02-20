import streamlit as st
import json
import urllib.request
import pandas as pd
import pymongo
import plotly.express as px
import plotly.graph_objects as go
import warnings
warnings.filterwarnings('ignore')

st.set_page_config(page_title="Registered Vehicles", page_icon=":bar_chart:",layout="wide")
st.title(" :bar_chart: Registered Vehicles EDA")

st.markdown('<style>div.block-container{padding-top:1rem;}</style>',unsafe_allow_html=True)

# Getting dataset from MongoDB database
client = pymongo.MongoClient("mongodb+srv://tsubedy:TS24751@cluster1.ppbek.mongodb.net/?retryWrites=true&w=majority")
db = client["Registered_Vehicles_db"]
collection = db.Registered_Vehicles
cursor = collection.find()
Registered_Vehicles = list(cursor)
US_Registered_Vehicles = pd.DataFrame(Registered_Vehicles, columns =['year', 'state', 'auto', 'bus', 'truck', 'motorcycle'])

# US_Registered_Vehicles['year'] = pd.to_datetime(US_Registered_Vehicles['year'], format='%Y')

# US_Registered_Vehicles = US_Registered_Vehicles.astype({'auto': 'float64', 'bus': 'float64', 'truck': 'float64', 'motorcycle': 'float64'})
US_Registered_Vehicles = US_Registered_Vehicles.astype({'year': 'int', 'state': 'object', 'auto': 'float64', 'bus': 'float64', 'truck': 'float64', 'motorcycle': 'float64'})

# Aggregating the vehicle types by year
US_Registered_Vehicles = US_Registered_Vehicles.groupby(["year"]).agg({"auto":'sum',"truck":'sum', "bus":'sum',"motorcycle":'sum'})

col1, col2 = st.columns((2))

# Getting the min and max date 
startDate = US_Registered_Vehicles.index.min()
endDate = US_Registered_Vehicles.index.max()

with col1:
    st.subheader("Seletion of Strating years")
    date1 = st.number_input("Start Year", startDate)

with col2:
    st.subheader("Seletion of Ending Year")
    date2 = st.number_input("End Year", endDate)


US_Registered_Vehicles = US_Registered_Vehicles[(US_Registered_Vehicles.index >= date1) & (US_Registered_Vehicles.index <= date2)].copy()

st.sidebar.header("Choose your filter: ")

# Create for State
state = st.sidebar.multiselect("Statewise Data", US_Registered_Vehicles["state"].unique())

if not state:
    df2 = US_Registered_Vehicles.copy()
else:
    df2 = US_Registered_Vehicles[US_Registered_Vehicles["state"].isin(state)]





# Download orginal DataSet
csv = US_Registered_Vehicles.to_csv(index = False).encode('utf-8')
st.download_button('Download Data', data = csv, file_name = "Data.csv",mime = "text/csv")





