import os
import sqlite3
from urllib import parse
from sqlalchemy import create_engine
import pandas as pd
from datetime import datetime


database = "Warehouse"

# The below code defines a function to retrieve a pandas dataframe from a select statement on sql18

def sql18_dataframe(database, sql):

    user = os.environ["CHAT_USER"]
    passw = os.environ["CHAT_PASS"]
    server = "WHServer"

    connection_string = f"""
    DRIVER={{SQL SERVER}};
    SERVER={server};
    DATABASE={database};
    UID={user};
    PWD={passw};
    """

    params = parse.quote_plus(connection_string)
    engine = create_engine(f"mssql+pyodbc:///?odbc_connect={params}")
    conn = engine.connect()

    try:
        df = pd.read_sql_query(sql, conn)
    except Exception as e:
        print(
            f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} - An unexpected error occurred: {e}'
        )
        df = None
    finally:
        conn.close()

    return df


def create_datbase():

# The below code reads in a sql file and splits the file down into each sql statement to be executed and inserted into the sqllite3 database.

    with open("Insert Table Queries.sql", "r") as file:
        insert_sql = file.read()

    insert_statements_sql = insert_sql.split(";")

    country_insert_sql = insert_statements_sql[0].strip()
    customer_insert_sql = insert_statements_sql[1].strip()
    sales_insert_sql = insert_statements_sql[2].strip()
    item_insert_sql = insert_statements_sql[3].strip()
    date_insert_sql = insert_statements_sql[4].strip()
    brand_insert_sql = insert_statements_sql[5].strip()
    purchase_insert_sql = insert_statements_sql[6].strip()
    orderbook_insert_sql = insert_statements_sql[7].strip()
    inventory_insert_sql = insert_statements_sql[8].strip()

#The below code creates the pandas dateframe needed for inserting the data into new tables

    df_country = sql18_dataframe(database, country_insert_sql)
    df_customer = sql18_dataframe(database, customer_insert_sql)
    df_sales = sql18_dataframe(database, sales_insert_sql)
    df_item = sql18_dataframe(database, item_insert_sql)
    df_date = sql18_dataframe(database, date_insert_sql)
    df_brand = sql18_dataframe(database, brand_insert_sql)
    df_purchase = sql18_dataframe(database, purchase_insert_sql)
    df_orderbook = sql18_dataframe(database, orderbook_insert_sql)
    df_inventory = sql18_dataframe(database, inventory_insert_sql)

# The code below drops and recreates the shiner sqllite3 database and creates the tables needed

    if os.path.exists("Chat.db"):
        os.remove("Chat.db")

    with open("Create Tables.sql", "r") as file:
        create_tables_query = file.read()

    conn = sqlite3.connect("Chat.db")
    cursor = conn.cursor()

    sql_statements = create_tables_query.split(";")

    for statement in sql_statements:
        if statement.strip() != "":
            cursor.execute(statement)

    conn.commit()

    df_country.to_sql('Country', conn, if_exists='append', index=False, chunksize=1000)
    df_customer.to_sql('Customers', conn, if_exists='append', index=False, chunksize=1000)
    df_sales.to_sql('Sales', conn, if_exists='append', index=False, chunksize=1000)
    df_item.to_sql('Items', conn, if_exists='append', index=False, chunksize=1000)
    df_date.to_sql('Date', conn, if_exists='append', index=False, chunksize=1000)
    df_brand.to_sql('Brand', conn, if_exists='append', index=False, chunksize=1000)
    df_purchase.to_sql('Purchases', conn, if_exists='append', index=False, chunksize=1000)
    df_orderbook.to_sql('Orderbook', conn, if_exists='append', index=False, chunksize=1000)
    df_inventory.to_sql('Inventory', conn, if_exists='append', index=False, chunksize=1000)

    conn.close()
    
    print(
        f'{datetime.now().strftime("%Y-%m-%d %H:%M:%S")} - sqlite3 database has been created'
    )