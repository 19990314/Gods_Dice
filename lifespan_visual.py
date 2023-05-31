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
        converted_element["content"] = events_df.iloc[key1]["event"]
        converted_element["content"] += "(age: "+ str(int(events[(key1,key2)][1])) + ")"
        # date
        converted_element["start"] = key2.strftime("%Y-%m-%d")
        container.append(converted_element)
    return container


# input
events = {(0, datetime.date(22, 3, 3)): [1, 20.547029036939648, 'prenatal'], (1, datetime.date(25, 8, 21)): [1, 24.017209111134036, 'prenatal'], (9, datetime.date(64, 3, 26)): [1, 62.63923293619273, 'prenatal']}
items = format_convert(events)

# construct UI
st.set_page_config(layout="wide")
timeline = st_timeline(items, groups=[], options={}, height="300px")
st.subheader("Selected item")
st.write(timeline)