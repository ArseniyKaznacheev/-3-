import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import psycopg2

st.title('Here you can check our shops')
conn = psycopg2.connect(dbname='postgres', user='postgres', 
                        password='1234', host='127.0.0.1')
conn.autocommit = True

with conn.cursor() as cursor:
    cursor.execute(
        """SELECT DISTINCT shop_name
        FROM shops"""
        )
    option_names = [i[0] for i in cursor.fetchall()]

option = st.radio("Pick an Shop",option_names, key = "opt")

#st.session_state.opt

with conn.cursor() as cursor:
    cursor.execute(
        """SELECT open_time, close_time, address, latitude, longitude
        FROM shops
        Where shop_name = %(p1)s""", {'p1':st.session_state.opt}
        )
    time = cursor.fetchall()

st.write("Opening hours:")
st.write(str(time[0][0])[:5],' - ', str(time[0][1])[:5])
st.write("Address:")
st.write(time[0][2])

df1 = pd.DataFrame(
        [[float(time[0][3]), float(time[0][4])]],
        columns=["lat", "lon"],
    )

st.map(df1,color = "#ffaa00", size = 100)



@st.dialog("Our Shops")
def vote():
    with conn.cursor() as cursor:
        cursor.execute(
        """SELECT latitude, longitude
        FROM shops"""
            )
        df = pd.DataFrame(
            [[float(i[0]), float(i[1])] for i in cursor.fetchall()],
            columns=["lat", "lon"],
        )
    st.map(df,color = "#ffaa00", size = 1000)
if st.button("See all stores"):
    vote()

