import streamlit as st

# Set the title of the page
st.set_page_config(layout="wide")
st.title("My Tabbed Interface")


st.markdown(
    """
    <style>
    .stButton>button {
        background-color: transparent;
        border: blue;
        padding: 10px 15px;
        font-size: 19px;
        cursor: pointer;
    }
    .stButton>button:focus {
        outline: none;
    }
    .stApp {
        background-color: #f1f1f1;
        font-family: Arial, sans-serif;
        margin: -1px;
    }
    
    </style>
    """,
    unsafe_allow_html=True
)



# Create tabs
tabs = ["Home", "Tab 2", "Tab 3"]

# Create columns for tabs
col1, col2, col3 = st.columns(3)

# Render tabs in the columns
with col1:
    if st.button(tabs[0]):
        selected_tab = tabs[0]

with col2:
    if st.button(tabs[1]):
        selected_tab = tabs[1]

with col3:
    if st.button(tabs[2]):
        selected_tab = tabs[2]

if 'selected_tab' not in locals():
    selected_tab = tabs[0]

# Render content based on the selected tab
if selected_tab == "Home":
    st.header("Tab 1 Content")
    st.write("This is the content of Tab 1. There is a option to put here all the contents about wastewater")
elif selected_tab == "Tab 2":
    st.header("Tab 2 Content")
    st.write("This is the content of Tab 2.")
elif selected_tab == "Tab 3":
    st.header("Tab 3 Content")
    st.write("This is the content of Tab 3.")



st.markdown(""" <style>[data-testid="stSidebar"][aria-expanded="true"] > div:first-child {width: 280px;}
    [data-testid="stSidebar"][aria-expanded="false"] > div:first-child {width: 280px;margin-left: -300px;}
    </style>""", unsafe_allow_html=True,)