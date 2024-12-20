import psycopg2

conn = psycopg2.connect(dbname='postgres', user='postgres', 
                        password='1234', host='127.0.0.1')
conn.autocommit = True

with conn.cursor() as cursor:
    cursor.execute(
        """Drop TABLE if exists users CASCADE;
           Drop TABLE if exists products CASCADE;
           Drop TABLE if exists shops CASCADE;
           Drop TABLE if exists count_in_shop CASCADE;
           Drop TABLE if exists manufacturer CASCADE;
           Drop TABLE if exists reviews CASCADE;
           Drop TABLE if exists shop_comm CASCADE;"""
        )
conn.close()


