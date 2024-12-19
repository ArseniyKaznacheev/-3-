from turtle import onclick
import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import psycopg2
import pandas.io.sql as sqlio
import time

conn = psycopg2.connect(dbname='postgres', user='postgres', 
                        password='1234', host='127.0.0.1')
conn.autocommit = True

def f():
    st.session_state.ins = True

if 'ins' not in st.session_state:
    st.session_state['ins'] = None
if 'name' not in st.session_state:
    st.session_state["name"] = None
if 'man' not in st.session_state:
    st.session_state['man'] = None

def name_ch():
    st.session_state["name"] = False

st.title("Here you can add products and check statistics:")
with conn.cursor() as cursor:
    cursor.execute(
        """SELECT DISTINCT product_type
        FROM products"""
    )
    mass = []
    a = cursor.fetchall()
    for i in range(len(a)):
        mass.append(a[i][0])


    option_names1 = ["Addit", "Stat"]
    option1 = st.radio("Pick an option",option_names1, key = "opt1")

    if option1 == "Addit":
        #st.session_state["name"] = None

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

###
    
        #time.sleep(2)

        if 'type' not in st.session_state:
            st.session_state['ins'] = None
            name = st.text_input("Product name:")
            st.session_state['ins'] = None
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
            name = st.selectbox("existing or new Product", name_list,index=None, key = 'ins')

            st.session_state["name"] = False

            if name == 'New Item':
                name = st.text_input("Product name:")
                st.session_state.name = True


        #st.session_state.name
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
        else:
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
        country_list = ['Russia','Belarus', 'China', 'Germany', 'France', 'Belgium', 'US', 'Bangladesh', 'Turkey']
        pr_name = ['current price', 'Change price']

        #st.session_state.name
        #st.session_state.ins
        if not st.session_state.name and st.session_state.ins and st.session_state.type != 'New type':
            price_opt = st.radio("Price", pr_name, key = 'pr_opt')
            if st.session_state.pr_opt == 'Change price':
                price = st.number_input("Price", min_value=0.00, max_value=9999999.00, step=1.00)
            else:
                with conn.cursor() as cursor:
                    cursor.execute(
                        """SELECT price 
                        FROM products
                        WHERE product_name = %(p1)s""", {'p1':name}
                        )
                    pr = cursor.fetchall()[0][0]
                st.write("Current price is:")
                st.write(pr)
                price = pr
        else:
            price = st.number_input("Price", min_value=0.00, max_value=9999999.00, step=1.00)
     #   st.session_state.name
     #   st.session_state.type
        if st.session_state.name or st.session_state.type == 'New type':
            man = st.selectbox("Manufacturer:", man_list,index=None, key ='man')
            if man == 'New Manufacturer':
                man = st.text_input("Add new nanufacturer:")
                country = st.selectbox("Manufacturer country", country_list, index=None, key = 'country')
        shop = st.selectbox('Select a shop', shops_list,index=None, key = 'shop')
        
        val = 0;
##
        #st.session_state.name
        if st.session_state.shop != None:
            #st.session_state.shop
            #st.session_state.name
            #st.session_state.name
            with conn.cursor() as cursor:
                    cursor.execute(
                        """SELECT count FROM count_in_shop
                        WHERE shop_id = (SELECT shop_id FROM shops WHERE shop_name = %(p1)s)
                        AND product_id = (SELECT product_id FROM products WHERE product_name = %(p2)s);""",
                            {'p1': st.session_state.shop, 'p2': name}
                        )
                    val = cursor.fetchall()
            #st.write(val)
            if len(val)>0:
                val = val[0][0]
            else:
                val = 0
            #st.write(val)
        count = st.slider("Count of product", min_value=0, max_value=400, value= val, step=1)



        if st.button("Add to database"):
            with conn.cursor() as cursor:
                    cursor.execute(
                        """SELECT product_name
                        FROM products
                        Where product_name = %(p1)s""", {'p1':name}
                        )
                    base_name = cursor.fetchall()

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
            #elif st.session_state.type == 'New type' and st.session_state.country == None:
             #   st.warning("Please enter thr manufacturer's country")
            elif len(str(name)) > 70:
                st.warning("Please enter shorter name(max is 70 symbols)")
            elif st.session_state.name and len(str(man)) > 100:
                st.warning("Please enter shorter manufactirer name (max is 100 symbols)")

            else:
                with conn.cursor() as cursor:
                    cursor.execute(
                            """SELECT product_id, product_name, price, manufacturer_id
                            FROM products
                            WHERE product_name = %(p1)s;""", {'p1': name}
                            )
                    prod_info = cursor.fetchall()
                    prod_info = [i[0] for i in prod_info]
                    #st.write(prod_info)

                if len(prod_info) == 0:

                    with conn.cursor() as cursor:
                        cursor.execute(
                        """SELECT name
                        FROM manufacturer
                        WHERE name = %(p1)s;""", {'p1':man}
                            )
                        man_name = cursor.fetchall()

                    if len(man_name) == 0:
                        with conn.cursor() as cursor:
                            cursor.execute(
                                    """INSERT INTO manufacturer(name, country) VALUES
                                    (%(p1)s, %(p2)s);""", {'p1':man, 'p2':country}
                                )
                    with conn.cursor() as cursor:
                        cursor.execute(
                            """SELECT manufacturer_id 
                            FROM manufacturer
                            WHERE name = %(p1)s;""", {'p1':man}
                            )
                        man_id = cursor.fetchall()[0][0]

                    with conn.cursor() as cursor:
                        cursor.execute(
                            """INSERT INTO products(product_name, product_type, price, manufacturer_id) VALUES
                            (%(p1)s, %(p2)s, %(p3)s, %(p4)s);
                            """, {'p1': name, 'p2' : type1, 'p3' : price,'p4':man_id}
                        )
                    with conn.cursor() as cursor:
                        cursor.execute(
                            """SELECT product_id
                            FROM products
                            WHERE product_name = %(p1)s;""", {'p1': name}
                            )
                        prod_id = cursor.fetchall()[0][0]
                        cursor.execute(
                            """SELECT DISTINCT shop_id
                            FROM shops;"""
                            )
                        shops_list = [i[0] for i in cursor.fetchall()]
                        cursor.execute(
                            """SELECT DISTINCT shop_id
                            FROM shops
                            Where shop_name = %(p1)s;""", {'p1':shop}
                            )
                        shop_id = cursor.fetchall()[0][0]

                    for i in shops_list:
                        if i != shop_id:
                            with conn.cursor() as cursor:
                                cursor.execute(
                                    """INSERT INTO count_in_shop(shop_id, product_id, count) VALUES
                                    (%(p1)s, %(p2)s,0);""", {'p1': i, 'p2': prod_id}
                                    )
                        else:
                            with conn.cursor() as cursor:
                                cursor.execute(
                                    """INSERT INTO count_in_shop(shop_id, product_id, count) VALUES
                                    (%(p1)s, %(p2)s,%(p3)s);""", {'p1': i, 'p2': prod_id,'p3':count}
                                    )
                else:
                    if st.session_state.name or st.session_state.type == 'New type':
                        st.warning("This Item has already been added")
                        time.sleep(2)
                        st.rerun()
                    if st.session_state.pr_opt == "Change price":
                        with conn.cursor() as cursor:
                            cursor.execute(
                                """UPDATE products
                                SET price = %(p1)s
                                WHERE product_name = %(p2)s""", {'p1':price, 'p2':name}
                                )
                    with conn.cursor() as cursor:
                        cursor.execute(
                            """SELECT DISTINCT shop_id
                            FROM shops
                            Where shop_name = %(p1)s;""", {'p1':shop}
                            )
                        shop_id = cursor.fetchall()[0][0]
                    with conn.cursor() as cursor:
                        cursor.execute(
                            """SELECT product_id
                            FROM products
                            WHERE product_name = %(p1)s;""", {'p1': name}
                            )
                        prod_id = cursor.fetchall()[0][0]
                    with conn.cursor() as cursor:
                        cursor.execute(
                            """UPDATE count_in_shop
                            SET count = %(p1)s
                            WHERE shop_id = %(p2)s and product_id = %(p3)s;""", {'p1':count, 'p2':shop_id, 'p3':prod_id}    
                        )

                st.success("Product was added to base")
    else:
        sql = """SELECT product_type, ROUND(AVG(price), 2) as avg_price
                FROM products
                GROUP BY product_type;"""
        dat = sqlio.read_sql_query(sql, conn)
        dat




