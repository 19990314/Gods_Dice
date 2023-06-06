import streamlit as st
from streamlit_timeline import st_timeline
import datetime
from person import *

def format_convert(events):
    id = 1
    container = []
    for key1, key2 in events:
        converted_element = {}
        converted_element["id"] = id
        id += 1
        # output content
        converted_element["content"] = events_df.iloc[key1-1]["event"]
        converted_element["content"] += "(age: "+ str(int(events[(key1,key2)][1])) + ")"
        # date
        converted_element["start"] = key2.strftime("%Y-%m-%d")
        container.append(converted_element)
    return container


# input
events = {(12, datetime.date(1, 3, 7)): [1, 0, 'birthday'], (9, datetime.date(39, 2, 26)): [1, 38.0, 'prenatal'], (5, datetime.date(65, 2, 19)): [1, 64.0, 'prenatal'], (10, datetime.date(77, 2, 16)): [1, 76.0, 'prenatal']}
items = format_convert(events)

# construct UI
st.set_page_config(layout="wide")
timeline = st_timeline(items, groups=[], options={}, height="300px")
st.subheader("Selected item")
st.write(timeline)