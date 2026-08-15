import threading
import queue
import os
import mysql.connector
from mysql.connector import Error
import dotenv

dotenv.load_dotenv(".env")

global query_queue
global result_queue

query_queue = queue.Queue()
result_queue = queue.Queue()

def SQLHandler():
    host = dotenv.get_key(".env", "MYSQL_HOST")
    user = dotenv.get_key(".env", "MYSQL_USER")
    password = dotenv.get_key(".env", "MYSQL_PASSWORD")
    database = dotenv.get_key(".env", "MYSQL_DATABASE")

    try:
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database,
            charset='utf8mb4',
            collation='utf8mb4_unicode_ci'
        )

        print("[SQLHANDLER] Connected to MySQL")

    except Error as e:
        print(f"[SQLHANDLER] Connection failed: {e}")
        return

    while True:

        query, params, result_queue = query_queue.get()

        if query:
            try:
                cursor = connection.cursor()

                cursor.execute(query, params)

                # Queries that return rows
                if cursor.with_rows:
                    result = cursor.fetchall()
                else:
                    connection.commit()
                    result = None

                result_queue.put(result)

                cursor.close()

            except Exception as e:
                result_queue.put(e)

            finally:
                query_queue.task_done()

            print(f"[SQLHANDLER] Executed query: {query}")
        else:
            print("[SQLHANDLER] Received empty query, skipping.")


# Start SQL worker
sql_thread = threading.Thread(
    target=SQLHandler,
    daemon=True
)

sql_thread.start()

def put_query(query, params=None):
    result_queue = queue.Queue(maxsize=1)

    query_queue.put((query, params, result_queue))

    result = result_queue.get(timeout=30)

    print(f"[SQLHANDLER] Result: {result}")

    if isinstance(result, Exception):
        return None

    if result is None:
        return "None"
    else:
        return result