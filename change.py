import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import psycopg2
import pandas.io.sql as sqlio


def name_state():
    st.session_state["name"] = False

conn = psycopg2.connect(dbname='postgres', user='postgres', 
                        password='1234', host='127.0.0.1')
conn.autocommit = True


st.title("Here you can add products and check statistics:")
option_names1 = ["Addit", "Stat"]
option1 = st.radio("Pick an option",option_names1, key = "opt1")

if option1 == "Addit":
    
    with conn.cursor() as cursor:
        cursor.execute(
                """SELECT shop_name
                FROM shops"""
            )
        shops_list = [i[0] for i in cursor.fetchall()]

    with conn.cursor() as cursor:
        cursor.execute(
                """SELECT DISTINCT product_type
                FROM products"""
            )
        prod_list = [i[0] for i in cursor.fetchall()]
        prod_list.append('New type')


       
    if 'type' not in st.session_state:
        name = st.text_input("Product name:")
        st.session_state["name"] = False
    elif st.session_state.type == 'New type':
        name = st.text_input("Product name:")
        st.session_state["name"] = False
    else:
        with conn.cursor() as cursor:
            cursor.execute(
                    """SELECT DISTINCT product_name 
                    FROM products
                    Where product_type = %(p1)s""", {'p1':st.session_state.type}
                )
            name_list = [i[0] for i in cursor.fetchall()]
            name_list.append('New Item')
            name = st.selectbox("existing or new Product", name_list,index=None)
            st.session_state.name = False
        if name == 'New Item':
            name = st.text_input("Product name:")
            st.session_state.name = True
    with conn.cursor() as cursor:
        cursor.execute(
                        """SELECT product_name, product_type, price, manufacturer_id
                        FROM products
                        Where product_name = %(p1)s""", {'p1':name}
            )
        prod_info = cursor.fetchall()
    if len(prod_info) == 0:

        #Добавляем в базу
        type1 = st.selectbox("Product type:", prod_list,index=None, key='type')

        if type1 == 'New type':
            type1 = st.text_input("Add new type:")


            with conn.cursor() as cursor:
                cursor.execute(
                    """SELECT DISTINCT name
                    FROM manufacturer"""
                )
                man_list = [i[0] for i in cursor.fetchall()]
                man_list.append('New Manufacturer')
        elif st.session_state.type != None:
            with conn.cursor() as cursor:
                cursor.execute(
                    """SELECT DISTINCT name
                    FROM manufacturer
                    WHERE manufacturer_id in
                    (SELECT manufacturer_id FROM products
                    Where product_type = %(p1)s)""", {'p1':type1}
                )
                man_list = [i[0] for i in cursor.fetchall()]
                man_list.append('New Manufacturer')
        man = st.selectbox("Manufacturer:", man_list,index=None, key ='man')
        if man == 'New Manufacturer':
            man = st.text_input("Add new nanufacturer:")
            country_list = ['Russia','Belarus', 'China', 'Germany', 'France', 'Belgium', 'US', 'Bangladesh', 'Turkey']
            co_opt = st.selectbox("Country", country_list, index=None)

        price = st.number_input("Price", min_value=0.00, max_value=9999999.00, step=1.00)
        count = st.slider("Count of product", min_value=1, max_value=400, value=1, step=1)
        shop = st.selectbox('Select a shop', shops_list,index=None, key = 'shop')



        if st.button("Add to database"):

            if name is None:
                st.warning("Write Product name")
            elif len(name) < 1:
                 st.warning("Write Product name")
            elif type1 is None:
                st.warning("Select type")
            elif len(type1) < 1:
                 st.warning("Select type")
            elif shop is None:
                st.warning('Select shop')
            elif price > 9999999:
                st.warning("The price is too high")
            elif st.session_state.type is None:
                st.warning("Select the Shop please")
            elif st.session_state.man is None and st.session_state.name:
                st.warning("Select the Manufacturer please")
            elif len(str(name)) > 70:
                st.warning("Please enter shorter name(max is 70 symbols)")
            elif st.session_state.name and len(str(man)) > 100:
                st.warning("Please enter shorter manufactirer name (max is 100 symbols)")

            else:







if option1 == "Stat":
    sql = """SELECT product_type, ROUND(AVG(price), 2) as avg_price
            FROM products
            GROUP BY product_type;"""
    dat = sqlio.read_sql_query(sql, conn)
    dat



