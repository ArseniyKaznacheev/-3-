from email.mime import image
import re
import streamlit as st
import streamlit_authenticator as stauth
import time
import psycopg2
from psycopg2.extras import DictCursor
import hashlib
import pickle
from pathlib import Path

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from PIL import Image
from streamlit_image_select import image_select
from annotated_text import annotated_text
from streamlit_star_rating import st_star_rating
import random
import traceback



conn = psycopg2.connect(dbname='postgres', user='postgres', 
                        password='1234', host='127.0.0.1')
conn.autocommit = True


#if "reg" not in st.session_state:
 #   st.session_state["reg"] = False
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "reg" not in st.session_state:
    st.session_state["reg"] = False
if "log" not in st.session_state:
    st.session_state["log"] = False
if "admin" not in st.session_state:
    st.session_state['admin'] = False
if 'er' not in st.session_state:
    st.session_state['er'] = False
if  'username' not in st.session_state:
    st.session_state.username = None

def reg_page(): 
    st.title("Registration")
    st.text_input(label="Enter Username", key = "un")
    st.text_input(label="Enter password", key = "pas")
    if st.button("registrate me"):
        username1 = st.session_state["un"]
        passw1 = st.session_state["pas"]
        if username1 == "" or passw1 == "":
            st.warning("Please enter Username and Password")
            st.rerun()
        elif len(username1) > 20 or len(passw1) > 20:
            st.warning("Please enter shorter Username or Password (max length is 20 symbols)")
            st.rerun()
        with conn.cursor() as cursor:
            cursor.execute(
                    """SELECT username
                    FROM users
                    WHERE username = %s;""",(username1, )
            )
            if len(cursor.fetchall()) == 0:
                pas1 = hashlib.sha256(passw1.encode()).hexdigest()
                with conn.cursor() as cursor:
                    cursor.execute(
                            """INSERT INTO users(username, pass, role)
                            VALUES
                            (%(p1)s, %(p2)s, 'viewer');
                            """, {'p1': username1, 'p2' : pas1}
                    )
                st.success('You have been registered')
            else:
                st.warning("That username is already taken")
            
    st.rerun()
    
def log_check():
    username2 = st.session_state["l_un"]
    passw2 = st.session_state["l_pas"]
    if username2 == "" or passw2 == "":
        st.warning("Please enter Username and Password")

    with conn.cursor() as cursor:
        cursor.execute(
                    """SELECT username
                    FROM users
                    WHERE username = %s;""",(username2, )
        )
        usn = cursor.fetchall()
    if len(usn) == 0:
        st.warning("There is no user with this login")

    else:
        pas2 = hashlib.sha256(passw2.encode()).hexdigest()
        with conn.cursor() as cursor:
            cursor.execute(
                    """SELECT pass
                    FROM users
                    WHERE username = %s;""",(username2, )
            )
            passw = cursor.fetchall()[0][0]
        if passw == pas2:
            st.success(f'Welcome, {username2}!!!')
            st.session_state.username = username2
            st.session_state.logged_in = True
            st.session_state["log"] = False
            with conn.cursor() as cursor:
                cursor.execute(
                    """SELECT role
                    FROM users
                    WHERE username = %s;""",(username2, )
                )
                role = cursor.fetchall()[0][0]
                if role == 'employee':
                    st.session_state.admin = True
                else:
                    st.session_state.admin = False
            time.sleep(1)
        else:
            st.warning('Incorrect password')


        


def main():
    st.title("Main Page")
    #st.image("photos/too.jpg")

    if 'tab' not in st.session_state:
        st.session_state["tab"] = False
    
    with conn.cursor() as cursor:
        cursor.execute(
                """SELECT DISTINCT product_type
                FROM products"""
            )
        type_list = [i[0] for i in cursor.fetchall()]
        #type_list = cursor.fetchall()

    img_list = ["Furniture", "Lighting", "Textile", "Kitchen"]
 
    images = [("photos/" + i + ".jpg") if (i in img_list) else "photos/too.jpg" for i in type_list]

    img = image_select("Select product type", images = images, return_value = 'index', index = 0)
    #st.write(type_list[img])

    with conn.cursor() as cursor:
        cursor.execute(
            """SELECT product_name FROM products
            Where product_type = %(p1)s""", {'p1':type_list[img]}
            )
        prod = [i[0] for i in cursor.fetchall()]
    
    title = "Products by category: " + type_list[img]
    st.selectbox(title, prod, index=None, key='prod')

    if st.session_state.prod is not None:
        tab1, tab2, tab3 = st.tabs(["General information", "Manufacturer", "Comments"])
       
        with conn.cursor() as cursor:
            cursor.execute(
                    """SELECT product_id,  price, manufacturer_id FROM products
                    WHERE product_name = %(p1)s;""", {'p1':st.session_state.prod}
                )
            prod_info = cursor.fetchall()[0]


        with tab1:


            st.title("General information")
                #st.write(prod_info[0])
                #st.write(prod_info)
            annotated_text("Price......................", (str(prod_info[1]), "rub."))
            with conn.cursor() as cursor:
                cursor.execute(
                    """SELECT DISTINCT shop_name,  count
                    FROM (SELECT shop_id, count FROM count_in_shop shop WHERE product_id = %(prod_id)s) as A
                        INNER JOIN
                        (SELECT shop_id, shop_name FROM shops) as B
                        USING(shop_id)""", {"prod_id" :prod_info[0]}
                    )
                shops_list = cursor.fetchall()
                #shops_list = [[i[0], i[1]] for i  in cursor.fetchall()]

            st.header("Amount of product in our shops:")

            st.write("Shop/Count")
            for i in shops_list:
                annotated_text((str(i[0]),), str(i[1]).rjust(60 - len(str(i[0])), "_"))
            #st.write(shops_list)



        with tab2:


            st.title("Information about Manufacturer")
            with conn.cursor() as cursor:
                cursor.execute(
                    """SELECT name, country FROM manufacturer
                    WHERE manufacturer_id = %(p1)s""", {'p1':prod_info[2]}
                    )
                man = cursor.fetchall()[0]
            #st.write(man)
            if man[1] != None:    
                annotated_text("Manufacturer......................", (str(man[0]), str(man[1])))
            else:
                annotated_text("Manufacturer......................", (str(man[0]), "Unknown country"))

            st.write("See also other products from this manufacturer:")
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT product_name, rate
                    FROM (SELECT product_id, product_name FROM products WHERE manufacturer_id = %(p1)s) AS A
                    INNER JOIN
                    (SELECT product_id, AVG(rating) as rate FROM reviews GROUP BY product_id) AS B
                    USING(product_id)
                    """, {'p1': prod_info[2]}
                    )
                prod_of_man = cursor.fetchall()
                #st.write(prod_of_man)
                for i in prod_of_man:
                    col = "#faa"
                    if i[1] > 2.5:
                        col = "#fea"
                 
                    if i[1] > 4:
                        col = "#afa"

                    annotated_text((str(i[0]), str(round(i[1],1)), col ))



        with tab3:
            with conn.cursor() as cursor:
                cursor.execute(
                    """
                    SELECT username, commentary, rating, review_id
                    FROM
                    (
                    SELECT review_id, user_id, commentary, rating
                    FROM reviews
                    WHERE product_id = %(p1)s
                    )AS A
                    INNER JOIN
                    (SELECT username, user_id
                    FROM users) AS B USING (user_id)
                    ORDER BY review_id DESC
                    LIMIT 6""", {'p1': prod_info[0]}
                    )
                comm = cursor.fetchall()
                #comm = comm[:6]

            for i in comm:
                #annotated_text((str(i[0]),'', "#fea"))
                #r = str(random.random())
                st_star_rating(label = i[0], maxValue = 5, defaultValue = i[2], read_only = True, size = 17, key=str(i[3]))
                annotated_text((str(i[1]), '',"#c4eeff"))
                st.write("___")
            #st_star_rating(label = "a", maxValue = 5, defaultValue = 1, read_only = True, size = 17)
            #st_star_rating(label = "a", maxValue = 5, defaultValue = 1, read_only = True, size = 17)

            if st.session_state.logged_in:
                st_star_rating(label = "Please rate you experience", maxValue = 5, defaultValue = 0, key = "rating", size= 20)
                txt = st.text_area(label="Leave the comment", placeholder="your comment here...", key = 'comm1', height=120, max_chars=250)

                if st.button("send", key='send'):

                    if len(st.session_state.comm1) < 2:
                        st.warning("Write longer comment")
                       
                        time.sleep(2)
                        st.rerun()
                    with conn.cursor() as cursor:
                        cursor.execute(
                        """INSERT INTO reviews(user_id, commentary, rating, product_id) VALUES
                        (
                            (SELECT user_id FROM users
                            WHERE username = %(p1)s)
                        , %(p2)s, %(p3)s, %(p4)s)""",
                        {'p1': st.session_state.username,
                        'p2': st.session_state.comm1,
                        'p3': st.session_state.rating,
                        'p4': prod_info[0]}
                            )

                    st.success("Your comment has been sent")
                    st.rerun()

                #st.write(st.session_state.comm, st.session_state.rating)
            else:
                st.write("login to leave an comment")



        




def login():
    with st.sidebar:
        st.text_input(label="Enter Username", key = "l_un")
        st.text_input(label="Enter password", key = "l_pas")
        if st.button("Log in"):
            st.session_state["log"] = True
        if st.session_state["log"] == True:
            log_check()
        if st.button("Register"):
            st.session_state.reg = True
        if st.session_state.reg:
            reg_page()

    st.rerun()



def logout():
    if st.button("Log out"):
        st.session_state.logged_in = False
        st.session_state["log"] = False
        st.session_state["reg"] = False
        st.rerun()

try:
    if st.session_state.er:
        raise Exception("Сontact administrator to restore the database")
    reg_page1 = st.Page(reg_page)
    main_page = st.Page(main, title = "Main Page", icon=":material/thumb_up:")
    login_page = st.Page(login, title="Log in")
    logout_page = st.Page(logout, title="Log out", icon=":material/logout:")
    
    
    shops = st.Page(
        "shops.py", title="Our shops", icon=":material/dashboard:", default=True
    )
    change = st.Page(
        "trial.py", title="change", icon=":material/notification_important:"
    )
    
    backup = st.Page("backup.py", title="backup", icon=":material/history:")
    
    
    
    
    if st.session_state.logged_in:
        if st.session_state.admin:
            pg = st.navigation(
                {
                    "Account": [logout_page],
                    "Reports": [shops, main_page],
                    "Tools": [backup, change],
                }
            )
        else:
            pg = st.navigation(
                {
                    "Account": [logout_page],
                    "Сatalog": [shops, main_page],
                }
            )
    else:
        pg = st.navigation([login_page])
        main()
    
    pg.run()
except Exception as _ex:


    if not st.session_state.admin or not st.session_state["logged_in"]:
        st.session_state["logged_in"] = False
    st.error(_ex)
    if st.session_state.er == False:
        
    
        st.error(_ex)
        time.sleep(1000)
        st.session_state.er = True
        st.rerun()
    if not st.session_state.logged_in:
        st.text_input(label="Enter Username", key = "l_un1")
        st.text_input(label="Enter password", key = "l_pas1")

        if hashlib.sha256(st.session_state.l_pas1.encode()).hexdigest()== hashlib.sha256('admin'.encode()).hexdigest() and  st.session_state.l_un1=='admin':
            st.session_state.reg = False
            st.session_state["log"] = False
            st.session_state.logged_in = True
            st.session_state.admin = True
            
            st.rerun()
    if st.session_state.logged_in and st.session_state.admin:
        logout_page = st.Page(logout, title="Log out", icon=":material/logout:")
        backup = st.Page("backup.py", title="backup", icon=":material/history:")
        pg = st.navigation({
                    "Account": [logout_page],
                    "Tools": [backup],
                }
        )
        pg.run()

