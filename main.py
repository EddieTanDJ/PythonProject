# Navigation Page
import app1
import app2
import app3
import app4
import streamlit as stream

try:
    PAGES = {
        "Overall Statistics": app1,
        "Patient Cases": app2,
        "Data Decomp and Forecast": app3,
        "Prevention Tips Video": app4
    }
    stream.sidebar.title('Navigation')
    selection = stream.sidebar.radio("Go to", list(PAGES.keys()))
    page = PAGES[selection]
    page.app()

except IOError:
    stream.error("File is not found or file is opened. Please make sure your that file name is correct and it is placed "
                 "in the correct directory. Please remember to close it.")