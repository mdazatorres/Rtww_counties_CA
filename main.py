import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from plot_functions import plotRt, plotNconc



# Read the LaTeX document from a file


#with open("text_1.rtf", "r") as file:
#    latex_content = file.read()

# Render LaTeX document using st.markdown
#st.markdown(latex_content, unsafe_allow_html=True)

with open("text1.html", "r") as file:
    html_content1 = file.read()

with open("text2.html", "r") as file:
    html_content2 = file.read()

# Display the HTML content


# Set the title of the page
data_Rt = pd.read_csv('data/data_all_Rt.csv')
data_Rt['Date'] = pd.to_datetime(data_Rt['Date'])
st.set_page_config(layout="wide")
st.title("Analysis of wastewater data for California counties")

#padding: 10px 15px;
st.markdown(
    """
    <style>
    .stButton>button {
        background-color: #f1f1f1;
        border: blue;
        padding: 10px 50px;
        font-size: 16px;
        cursor: pointer;
    }
    .stButton>button:focus {
        outline: none;
    }
    .stApp {
        background-color: #ffffff;
        font-family: Arial, sans-serif;
        margin: -1px;
    }
    
    </style>
    """,
    unsafe_allow_html=True
)

# Create tabs
tabs = ["Rt estimations","Smoothing functions", "Outlier detection"]

# Create columns for tabs
col1, col2, col3 = st.columns(3)

with col1:
    if st.button(tabs[0]):
        st.session_state.selected_tab = tabs[0]

with col2:
    if st.button(tabs[1]):
        st.session_state.selected_tab = tabs[1]

with col3:
    if st.button(tabs[2]):
        st.session_state.selected_tab = tabs[2]

if 'selected_tab' not in st.session_state:
    st.session_state.selected_tab = tabs[0]


list_counties =list(np.unique(list(data_Rt.County.unique())))


# Render content based on the selected tab

if st.session_state.selected_tab == "Rt estimations":
    col1, _, col2,_= st.columns([0.14, 0.05,0.7,0.05])
    county = col1.selectbox('County', list_counties)  # Select a county
    col1.write('Rt computed with')
    ww_arima =col1.checkbox('Wastewater (ARIMA)', value=True)
    ww_trimmed =col1.checkbox('Wastewater (Trimmed)', value=False)
    cases =col1.checkbox('Cases', value=False)
    pr=col1.checkbox('Positivity Rate', value=False)
    data_county = data_Rt[data_Rt.County==county]

    end_date = data_county['Date'].max().to_pydatetime(); start_date = data_county['Date'].min().to_pydatetime()

    sl_init, sl_end = col2.slider('', min_value=start_date, max_value=end_date + timedelta(days=1),
                                      value=(start_date, end_date + timedelta(days=1)), format='MMM DD, YYYY')

    data_county_ = data_county[(data_county['Date'] >= sl_init) & (data_county['Date'] <= sl_end)]
    fig1=  plotRt(data_county=data_county_ , cases=cases, pr=pr, ww_arima=ww_arima,ww_trimmed=ww_trimmed)
    col2.plotly_chart(fig1, use_container_width=True)
    st.components.v1.html(html_content1, height=800, scrolling=True)


elif st.session_state.selected_tab == "Smoothing functions":
    st.write("Smoothing function")
    col1, _, col2, _ = st.columns([0.14, 0.05, 0.7, 0.05])
    county = col1.selectbox('County', list_counties)  # Select a county

    ww_arima = col1.checkbox('Wastewater (ARIMA)', value=True)
    ww_trimmed = col1.checkbox('Wastewater (Trimmed)', value=False)

    data_county = data_Rt[data_Rt.County == county]

    end_date = data_county['Date'].max().to_pydatetime();
    start_date = data_county['Date'].min().to_pydatetime()

    sl_init, sl_end = col2.slider('', min_value=start_date, max_value=end_date + timedelta(days=1),
                                  value=(start_date, end_date + timedelta(days=1)), format='MMM DD, YYYY')

    data_county_ = data_county[(data_county['Date'] >= sl_init) & (data_county['Date'] <= sl_end)]

    fig2 = plotNconc(data_county=data_county_, ww_arima=ww_arima, ww_trimmed=ww_trimmed)
    col2.plotly_chart(fig2, use_container_width=True)

    st.components.v1.html(html_content2, height=800, scrolling=True)

elif st.session_state.selected_tab == "Outlier detection":
    st.subheader("👷 Under Construction 👷")



st.markdown(""" <style>[data-testid="stSidebar"][aria-expanded="true"] > div:first-child {width: 280px;}
    [data-testid="stSidebar"][aria-expanded="false"] > div:first-child {width: 280px;margin-left: -300px;}
    </style>""", unsafe_allow_html=True,)

