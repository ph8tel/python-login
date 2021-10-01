
import psycopg2
import time as t
import os
db_url = os.environ.get("DATABASE_URL")
db_host = os.environ.get("DB_HOST")
db_user = os.environ.get("DB_USER")
db_pd = os.environ.get("DB_PD")

conn = psycopg2.connect(
        host = db_host,
        database = "dbgap98mhsiapi",
        user = db_user,
        password = db_pd)

def validate( username, pwd):
    with conn.cursor() as curs:
        curs.execute('''SELECT id 
    FROM users
    WHERE email = %s 
    AND password = crypt(%s, password);''', (username, pwd))
        data = curs.fetchone()


    return data

def just_sql( str):
    with conn.cursor() as curs:
        curs.execute(str)
        data = curs.fetchall()

    return data

def remove_user(name):
    with conn.cursor() as curs:
        result = curs.execute("DELETE FROM users WHERE email=%s", (name,))
        conn.commit()
        if result == 0:
            print("something went wrong")
        else:
            print("Delete successflu ", result)

def register( username, pwd):
    with conn.cursor() as curs:
        new_id = curs.execute(f"INSERT INTO users (email, password) VALUES (%s,crypt(%s, gen_salt('bf'))) RETURNING id;", (username, pwd))
        conn.commit()
        return new_id


print(just_sql("SELECT * FROM users;"))

