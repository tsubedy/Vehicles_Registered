import streamlit as st
import json
import urllib.request
import pandas as pd
import pymongo
import plotly.express as px
import plotly.graph_objects as go
import warnings
warnings.filterwarnings('ignore')
import config


st.set_page_config(page_title="Registered Vehicles", page_icon=":bar_chart:",layout="wide")
st.title(" :bar_chart: Registered Vehicles EDA")

st.markdown('<style>div.block-container{padding-top:1rem;}</style>',unsafe_allow_html=True)

# Getting dataset from MongoDB database
client = pymongo.MongoClient("mongodb+srv://{config.username}:{config.password}@cluster1.ppbek.mongodb.net/?retryWrites=true&w=majority")
db = client["Registered_Vehicles_db"]
collection = db.Registered_Vehicles
cursor = collection.find()


# Registered_Vehicles = list(cursor)
Registered_Vehicles = []
for document in cursor:
    Registered_Vehicles.append(document)

US_Registered_Vehicles = pd.DataFrame(Registered_Vehicles, columns =['year', 'state', 'auto', 'bus', 'truck', 'motorcycle'])

# US_Registered_Vehicles['year'] = pd.to_datetime(US_Registered_Vehicles['year'], format='%Y')

# US_Registered_Vehicles = US_Registered_Vehicles.astype({'auto': 'float64', 'bus': 'float64', 'truck': 'float64', 'motorcycle': 'float64'})
US_Registered_Vehicles_Year = US_Registered_Vehicles.astype({'year': 'int', 'state': 'object', 'auto': 'float64', 'bus': 'float64', 'truck': 'float64', 'motorcycle': 'float64'})

# Aggregating the vehicle types by year
US_Registered_Vehicles_Year = US_Registered_Vehicles_Year.groupby(["year"]).agg({"auto":'sum',"truck":'sum', "bus":'sum',"motorcycle":'sum'})

col1, col2 = st.columns((2))

# Getting the min and max date 
startDate = US_Registered_Vehicles_Year.index.min()
endDate = US_Registered_Vehicles_Year.index.max()

with col1:
    st.subheader("Strating Year")
    date1 = st.number_input("Start Year", startDate)

with col2:
    st.subheader("Ending Year")
    date2 = st.number_input("End Year", endDate)


US_Registered_Vehicles_Year = US_Registered_Vehicles_Year[(US_Registered_Vehicles_Year.index >= date1) & (US_Registered_Vehicles_Year.index <= date2)].copy()

st.sidebar.header("Choose Your Filters:")


# Create for State
selected_states = st.sidebar.multiselect("Select States ", US_Registered_Vehicles["state"].unique())

if not selected_states:
    US_Registered_Vehicles = US_Registered_Vehicles.copy()
else:
    US_Registered_Vehicles_State = US_Registered_Vehicles[US_Registered_Vehicles["state"].isin(selected_states)]


    
with col1:

# Define colors for each trace
    colors = ['blue', 'red', 'green', 'orange']

# Create a Plotly figure
    fig = go.Figure()

# Add traces with specified colors
    fig.add_trace(go.Scatter(x=US_Registered_Vehicles_Year.index, y=US_Registered_Vehicles_Year["auto"], mode='lines+markers', name='Auto', line=dict(color=colors[0])))
    fig.add_trace(go.Scatter(x=US_Registered_Vehicles_Year.index, y=US_Registered_Vehicles_Year["truck"], mode='lines+markers', name='Truck', line=dict(color=colors[1])))
    fig.add_trace(go.Scatter(x=US_Registered_Vehicles_Year.index, y=US_Registered_Vehicles_Year["bus"], mode='lines+markers', name='Bus', line=dict(color=colors[2])))
    fig.add_trace(go.Scatter(x=US_Registered_Vehicles_Year.index, y=US_Registered_Vehicles_Year["motorcycle"], mode='lines+markers', name='Motorcycle', line=dict(color=colors[3])))

# Update layout
    fig.update_layout(title="Yearly Registered Vehicles by Types", xaxis_title="Registered Years", yaxis_title="Number of Vehicles", legend=dict(x=0, y=1, traceorder="normal"))

# Render the Plotly figure within Streamlit
    st.plotly_chart(fig, use_container_width=True)


    
# with col2:

# # Grouping by both 'year' and 'state'
#     grouped_data = US_Registered_Vehicles.groupby(['year', 'state'])

#     # Applying aggregation functions as needed. For example, getting the sum of values for each group
#     summed_data = grouped_data.sum()

#     # Reset index to make 'year' and 'state' as columns
#     summed_data_reset = summed_data.reset_index()

#     # Create a scatter plot using Plotly Express
#     fig = px.scatter(summed_data_reset, x='year', y='auto', color='state',
#                      size='auto', hover_data=['truck', 'bus', 'motorcycle'],
#                      title='Registered Vehicles by Year and State',
#                      labels={'auto': 'Number of Auto Vehicles'},
#                      template='plotly_white')

#     # Update y-axis label
#     fig.update_yaxes(title_text='Number of Vehicles')

#     # Display the Plotly chart in Streamlit
#     st.plotly_chart(fig)

    
    
    
    
    
    
    



# Download orginal DataSet
csv = US_Registered_Vehicles.to_csv(index = False).encode('utf-8')
st.download_button('Download Original Data', data = csv, file_name = "Data.csv",mime = "text/csv")


