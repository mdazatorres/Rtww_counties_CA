from plot_functions import plotRt, plotNconc,plotNconc_data
import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta



# Call the function
data = [1, 2, 3, 4, 5]




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
tabs = ["Rt estimations","Data proccessing", "Analyze your data"]

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


elif st.session_state.selected_tab == "Data proccessing":

    col1, _, col2, _ = st.columns([0.14, 0.05, 0.7, 0.05])
    county = col1.selectbox('County', list_counties)  # Select a county

    col1.write("Smoothing function")
    ww_arima = col1.checkbox('ARIMA (1)', value=True)
    ww_trimmed = col1.checkbox('10d-trimmed ave)', value=False)

    data_county = data_Rt[data_Rt.County == county]

    end_date = data_county['Date'].max().to_pydatetime();
    start_date = data_county['Date'].min().to_pydatetime()

    sl_init, sl_end = col2.slider('', min_value=start_date, max_value=end_date + timedelta(days=1),
                                  value=(start_date, end_date + timedelta(days=1)), format='MMM DD, YYYY')

    data_county_ = data_county[(data_county['Date'] >= sl_init) & (data_county['Date'] <= sl_end)]

    fig2 = plotNconc(data_county=data_county_, ww_arima=ww_arima, ww_trimmed=ww_trimmed)
    col2.plotly_chart(fig2, use_container_width=True)

    st.components.v1.html(html_content2, height=800, scrolling=True)

elif st.session_state.selected_tab == "Analyze your data":
    st.markdown('### Upload an Excel or CSV file  ')
    st.write('Please upload an Excel or CSV file containing two columns: "Date" and "conc." The "conc" column should include the normalized or raw RNA concentration detected in wastewater.')
    col1, _, col2, _ = st.columns([0.4, 0.05, 0.4, 0.05])
    uploaded_file = col1.file_uploader("Upload Excel file", type=["xlsx"])
    if uploaded_file is not None:
        # Read the Excel file
        st.markdown('### Data proccesing  ')
        col1, _, col2, _ = st.columns([0.14, 0.05, 0.7, 0.05])

        df = pd.read_excel(uploaded_file)
        df['Date']= pd.to_datetime(df['Date'])
        end_date = df['Date'].max().to_pydatetime(); start_date = df['Date'].min().to_pydatetime()

        col1.write("Smoothing function")
        ww_arima = col1.checkbox('ARIMA (1)', value=True)
        ww_trimmed = col1.checkbox('10d-trimmed ave)', value=False)

        sl_init, sl_end = col2.slider('', min_value=start_date, max_value=end_date + timedelta(days=1),
                                      value=(start_date, end_date + timedelta(days=1)), format='MMM DD, YYYY')

        df_ = df[(df['Date'] >= sl_init) & (df['Date'] <= sl_end)]


        #mean = compute_mean(df)
        fig3=plotNconc_data(df_, ww_arima, ww_trimmed)
        col2.plotly_chart(fig3, use_container_width=True)

        st.markdown('### Rt estimation ')




        # tm < - 1: dim(data)[1]  # data[,"time"]
        # y < - log(data[, "SC2_N_norm_PMMoV"])
        # # y = ifelse(y==-Inf,NA,y)
        # ## fit the model
        # formula = y
        # ~f(z, model="ar1")
        # result = inla(formula, family="gaussian", data=list(y=y, z=tm))  # , E=E)
        # # summary(result)
        # # Cases respect to minimum concentration
        # wc = 1
        # # expected log concetration
        # yhat = exp(result$summary.fitted.values)
        # kk = wc / min(yhat$mean[yhat$mean > 0], na.rm = T)
        # k_av10 = wc / min(data$N_av10, na.rm = T)
        # # Recover cases from WW: proportional of cases
        # data$Cases_N_av10 = k_av10 * data$N_av10  # Cases from moving average
        # data$Cases_N = kk * yhat$mean  # Cases from INLA





st.markdown(""" <style>[data-testid="stSidebar"][aria-expanded="true"] > div:first-child {width: 280px;}
    [data-testid="stSidebar"][aria-expanded="false"] > div:first-child {width: 280px;margin-left: -300px;}
    </style>""", unsafe_allow_html=True,)

