import time
import uuid
from dbhandler import sql_handler

class UserControl:

    def create_user(username, password, email, phone, dob):
        uid = str(uuid.uuid4())
        if len(sql_handler.put_query(f"select * from users where username = '{username}';")) > 0:
            return 1
        query = "insert into users (id, username, password, email, phone, DoB, created) values (%s, %s, %s, %s, %s, %s, %s)"
        params = (uid, username, password, email, phone, dob, time.strftime('%Y-%m-%d %H:%M:%S'))
        result = sql_handler.put_query(query, params)
        if result is None:
            return 67
        else:
            return 0

    def get_user(uid):
        query = "select * from users where id = %s"
        params = (uid,)
        result = sql_handler.put_query(query, params)
        if result is None:
            return 67
        else:
            return result

    def delete_user(uid):
        query = "delete from users where id = %s"
        params = (uid,)
        result = sql_handler.put_query(query, params)
        if result is None:
            return 67
        else:
            return 0

    def update_user(uid, username=None, password=None, email=None, phone=None, dob=None):
        query = "update users set "
        params = []
        if username:
            query += "username = %s, "
            params.append(username)
        if password:
            query += "password = %s, "
            params.append(password)
        if email:
            query += "email = %s, "
            params.append(email)
        if phone:
            query += "phone = %s, "
            params.append(phone)
        if dob:
            query += "DoB = %s, "
            params.append(dob)
        query = query.rstrip(", ")
        query += " where id = %s"
        params.append(uid)
        result = sql_handler.put_query(query, tuple(params))
        if result is None:
            return 67
        else:
            return 0

    def get_uid(username):
        query = "select id from users where username = %s"
        params = (username,)
        result = sql_handler.put_query(query, params)
        if result is None:
            return 67
        else:
            return result[0][0]

    