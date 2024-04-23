import mysql.connector
from mysql.connector import Error

def query_data(host, port, database, user, password, query):
    """
    连接mysql,获取数据
    """
    try:
        connection = mysql.connector.connect(
            host=host,
            port=port,
            database=database,
            user=user,
            password=password
        )
        if connection.is_connected():
            cursor = connection.cursor()
            cursor.execute(query)
            records = cursor.fetchall()
            return records
    except Error as e:
        raise Exception("Error while connecting to MySQL") from e 
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def data_process(data):
    return data[3] + ":" + data[9]

def janitor_process(data):
    return data['description']
