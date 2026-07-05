
import streamlit as st
import pandas as pd

st.title("Netflix Data Analysis")

data = pd.DataFrame({
    "Type":["Movie","TV Show","Movie","Movie","TV Show"],
    "Year":[2020,2021,2019,2022,2023]
})

st.dataframe(data)
st.bar_chart(data["Type"].value_counts())
st.write("Content count by type")
