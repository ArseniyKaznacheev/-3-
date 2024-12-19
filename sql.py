import psycopg2
import hashlib
import pickle
from pathlib import Path
import random
import pandas.io.sql as sqlio
import numpy as np

try:
    conn = psycopg2.connect(dbname='postgres', user='postgres', 
                        password='1234', host='127.0.0.1')
    conn.autocommit = True
 
    with conn.cursor() as cursor:
        cursor.execute(
          """CREATE TABLE if not exists users(
            user_id serial PRIMARY KEY,
            username varchar(20) NOT NULL,
            pass varchar(100) NOT NULL,
            role varchar(8)
            );"""
        )
    with conn.cursor() as cursor:
        cursor.execute(
          """CREATE TABLE if not exists products(
            product_id serial PRIMARY KEY,
            product_name varchar(70) NOT NULL,
            product_type varchar(100),
            price NUMERIC(10,2),
            manufacturer_id integer
            );"""
        )
    with conn.cursor() as cursor:
        cursor.execute(
          """CREATE TABLE if not exists shops(
            shop_id serial PRIMARY KEY,
            shop_name varchar(25) NOT NULL,
            open_time time, 
            close_time time,
            longitude numeric(18,15),
            latitude numeric(18,15),
            address VARCHAR(150)
            );"""
        )
    with conn.cursor() as cursor:
        cursor.execute(
          """CREATE TABLE if not exists count_in_shop(
            shop_id integer NOT NULL,
            product_id integer NOT NULL,
            count integer
            );"""
        )
    with conn.cursor() as cursor:
        cursor.execute(
          """CREATE TABLE if not exists manufacturer(
            manufacturer_id serial PRIMARY KEY,
            name VARCHAR(20),
            country VARCHAR(10)
            );"""
        )
    with conn.cursor() as cursor:
        cursor.execute(
          """CREATE TABLE if not exists reviews(
            review_id serial PRIMARY KEY,
            product_id integer NOT NULL,
            user_id integer NOT NULL,
            commentary VARCHAR(1024),
            rating smallint
            );"""
        )
    with conn.cursor() as cursor:
        cursor.execute(
            """CREATE TABLE if not exists shop_comm(
            shop_id integer NOT NULL,
            review_id integer NOT NULL
            );"""
            )


    pas1 = "admin"
    pas2 = "1234"

    with conn.cursor() as cursor:
        cursor.execute(
            """INSERT INTO users(username, pass, role)
            VALUES
            ('admin', %(p1)s, 'employee'),
            ('cashier', %(p2)s, 'employee'),
            ('aaaa',%(p3)s, 'viewer');""", {'p1': hashlib.sha256(pas1.encode()).hexdigest(),
                                                  'p2': hashlib.sha256(pas2.encode()).hexdigest(),
                                                  'p3': hashlib.sha256('aaaa'.encode()).hexdigest()}
            )
    with conn.cursor() as cursor:
        cursor.execute(
            """INSERT INTO products(product_name, product_type, price, manufacturer_id)
            VALUES
            ( 
            'Blackout roller blind Inspire Santos 60x160 cm gray Granit 3',
            'Textile',900,1
            ),
            ( 
            'Blackout ribbon curtain Capital of Textiles Monaco 200x300 cm', 
            'Textile',3480,1
            ),

            ( 
            'Tulle on Madison ribbon 150x280 cm white', 
            'Textile', 320,1
            ),
            ( 
            'Veil 1 p/m 295 cm solid color white', 
            'Textile', 135,1
            ),
            ( 
            'Fabric 1 m/n canvas 300 cm color beige-gray', 
            'Textile', 930,2
            ),
            ( 
            'Polypropylene carpet Vision 83106 26 150x300 cm color beige', 
            'Textile', 4499,2
            ),
            ( 
            'Carpet Lugano 100x160 cm polypropylene 9540 color gray', 
            'Textile', 760,2
            ),

            (
            'LED ceiling chandelier Escada 10219/8LED 130W',
            'Lighting', 5491,3
            ),
            
            (
            'LED ceiling chandelier Escada Octans 10212/8',
            'Lighting', 6180,4
            ),
            
            (
            'Decorative lamp Start "Lava lamp"',
            'Lighting', 1428,4
            ),
            
            (
            'LED lamp Photon Wonderful lamp',
            'Lighting', 158,3
            ),
            
            (
            'Table lamp Rexant "Forte"',
            'Lighting', 1400,3
            ),
            
            (
            'LED table lamp Start CT808',
            'Lighting', 1111,3
            ),
            
            (
            'Hinged wardrobe Turin Light with 2 doors 100x200.6x37.2 cm',
            'Furniture', 7985,5
            ),
            
            (
            'Hinged wardrobe Lazurit 2 doors 100.6x176.2x51.3 cm',
            'Furniture', 11200,5
            ),
            
            (
            'TV stand Micon TVM-7 115x48x40.3 cm',
            'Furniture', 6501,5
            )
            
            ;"""
            )


    with conn.cursor() as cursor:
        cursor.execute(
            """INSERT INTO shops(shop_name, open_time, close_time,latitude, longitude, address)
            VALUES
            (
            'Altufyevo',
            '08:00:00', '23:00:00',55.917171544214014, 37.5776569841957, 
            'Moscow region, Mytishchi, Veshki village, ter. TPZ Altufyevo, building 3B'
            ),
            
            (
            'Warsaw highway',
            '07:00:00', '23:00:00',55.573496578052165, 37.60458390207371,
            'Moscow region, Leninsky district, rural settlement Bulatnikovskoye, Varshavskoe highway, 21st km, 25Yu/5'
            ),

            (
            'Vykhino',
            '07:00:00', '23:00:00',55.71758133296295, 37.83976591527733, 
            'Moscow, Novoukhtomskoe sh., 2A'
            ),
            
            (
            'Domodedovo',
            '07:00:00', '23:00:00',55.40136780318894, 37.77943186016109, 
            'Domodedovo, microdistrict Vostryakovo, st. Zaborie, 130'
            ),
            
            (
            'Zhukovsky',
            '08:00:00', '23:00:00',55.563389464418385, 38.05538939487529, 
            'Kulakovo village, Novoryazanskoe highway 37 km, 2'
            ),
            
            (
            'Zelenograd',
            '07:00:00', '23:00:00',56.00098196724519, 37.25253608244124, 
            'Moscow region, Leningradskoe highway, 37th kilometer, ow. 1nskoe highway 37 km, 2'
            ),
            
            (
            'ZIL',
            '08:00:00', '23:00:00',55.70035003827236, 37.64426455796639, 
            'Moscow, Likhacheva Ave., 15'
            )
            ;""", {'p1': hashlib.sha256(pas1.encode()).hexdigest(),
                                                  'p2': hashlib.sha256(pas2.encode()).hexdigest()}
        )
    with conn.cursor() as cursor:
        cursor.execute(
            """INSERT INTO manufacturer(name, country) VALUES
            ('Kostroma Textile', 'Russia'),
            ('Capital of textiles','Russia'),
            ('Inspire','China'),
            ('Lumin arte','China'),
            ('Anrex','Belarus');"""
            )

    with conn.cursor() as cursor:
        cursor.execute(
            """SELECT DISTINCT shop_id
            FROM shops"""
        )
        shops = [i[0] for i in cursor.fetchall()]
        sh_len = len(shops)

    with conn.cursor() as cursor:
        cursor.execute(
            """SELECT DISTINCT product_id
            FROM products"""
        )
        products = [i[0] for i in cursor.fetchall()]
        pr_len = len(products) 

    for i in shops:
        for j in products:
            if random.random() > 0.4:
                rand_num = int(abs(np.random.normal(30, 20, 1)))
            else:
                rand_num = 0
            with conn.cursor() as cursor:
                cursor.execute(
                    """INSERT INTO count_in_shop(shop_id, product_id, count) VALUES
                    (%(p1)s, %(p2)s, %(p3)s)""", {'p1':i, 'p2':j,'p3':rand_num}
                    ) 


    for i in range((pr_len * 3) + 1):
        shop = random.randint(0, sh_len)
        with conn.cursor() as cursor:
                cursor.execute(
                    """INSERT INTO shop_comm(shop_id, review_id) VALUES
                    (%(p1)s, %(p2)s)""", {'p1':shop,
                                          'p2': i}
                    )
    

    for i in range(1, pr_len+1):
        for j in range(4):
            rate = random.randint(0, 5)
            if rate > 3:
                comm = "I like it"
            else:
                comm = "I hate it"

            with conn.cursor() as cursor:
                cursor.execute(
                    """INSERT INTO reviews(user_id, commentary, rating, product_id) VALUES
                    (%(p1)s, %(p2)s, %(p3)s, %(p4)s)""", {'p1': j,
                                                          'p2': comm,
                                                          'p3': rate,
                                                          'p4': i}
                    )

except Exception as _ex:
    print("[INFO] ERROR228", _ex)
finally:
    if conn:
        conn.close()

