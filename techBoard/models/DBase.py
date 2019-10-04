# /models/DBase.py

# import pymysql

# def connection():
#     conn = pymysql.connect(host="localhost",
#                            user = "flaskUser",
#                            passwd = "Afton83110!",
#                            db = "svicars_wp")
#     c = conn.cursor(pymysql.cursors.DictCursor)

#     return c, conn


# PostgreSQL
import psycopg2
from psycopg2 import extras

def connection():
    conn = psycopg2.connect(host="localhost",database="database",user="user",password="password",options=f"--search_path={'schema'}")
    c = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
    return c, conn
