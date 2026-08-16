import time
import uuid
import argon2
from dbhandler import sql_handler

argonHasher = argon2.PasswordHasher()

class UserControl:

    def create_user(username, password, email, phone, dob):
        uid = str(uuid.uuid4())
        password = argonHasher.hash(password)
        if len(sql_handler.put_query("select * from users where username = %s;", (username,))) > 0:
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
        if result != []:
            if result is None:
                return 67
            else:
                return result
        else:
            return 1

    def delete_user(uid):
        query = "delete from users where id = %s"
        params = (uid,)
        result = sql_handler.put_query(query, params)
        if result is None:
            return 67
        else:
            return 0

    def update_user(uid, username=None, password=None, email=None, phone=None, dob=None, pfp_ref=None):
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
        if pfp_ref:
            query += "pfp_ref = %s, "
            params.append(pfp_ref)
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

    def validate_user(username, password):
        query = "select * from users where username = %s"
        params = (username,)
        result = sql_handler.put_query(query, params)
        if result is None:
            return 1
        else:
            hash = result[0][2]
            try:
                argonHasher.verify(hash, password)
                query = "update users set online = 1 where username = %s"
                params = (username,)
                result = sql_handler.put_query(query, params)
                return 0
            except:
                return 2

    def disconnect_user(id):
        query = "update users set online = 0 where id = %s"
        params = (id)
        result = sql_handler.put_query(query, params)
        if result is None:
            return 1
        else:
            return 0

    