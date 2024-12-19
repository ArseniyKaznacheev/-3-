import psycopg2

conn = psycopg2.connect(dbname='postgres', user='postgres', 
                        password='1234', host='127.0.0.1')
conn.autocommit = True

with conn.cursor() as cursor:
    cursor.execute(
        """Drop TABLE users;
           Drop TABLE products;
           Drop TABLE shops;
           Drop TABLE count_in_shop;
           Drop TABLE manufacturer;
           Drop TABLE reviews;
           Drop TABLE shop_comm;"""
        )
conn.close()


