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
events = {(7, datetime.date(1, 1, 13)): [1, 0.019178082191780823, 'afterbirth_passive'], (6, datetime.date(1, 2, 2)): [1, 0.07397260273972603, 'afterbirth_passive'], (8, datetime.date(1, 2, 11)): [1, 0.09863013698630137, 'afterbirth_passive'], (5, datetime.date(1, 3, 1)): [1, 0.14794520547945206, 'afterbirth_passive']}
items = format_convert(events)

# construct UI
st.set_page_config(layout="wide")
timeline = st_timeline(items, groups=[], options={}, height="300px")
st.subheader("Selected item")
st.write(timeline)