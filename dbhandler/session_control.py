import uuid
import datetime
import objects
from error_handler import ErrorCodes
from objects import OrbitSession
from dbhandler import sql_handler

error_codes = ErrorCodes()

class SessionControl:

    def create_session(user_id):
        sess_id = str(uuid.uuid4())
        created = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        sql_handler.put_query("update sessions set void = 1 where id = %s", (user_id,))
        query = "insert into sessions (sessid, id, created) values (%s, %s, %s)"
        params = (sess_id, user_id, created)
        result = sql_handler.put_query(query, params)
        if result is None:
            return error_codes.DB_ERROR
        else:
            return sess_id

    def validate_session(sess_id):
        query = "select void from sessions where sessid = %s"
        params = (sess_id,)
        result = sql_handler.put_query(query, params)
        if result is None:
            return error_codes.DB_ERROR
        else:
            if len(result) > 0 and result[0][0] == 0:
                return True
            else:
                return False

    def revoke_session(sess_id):
        query = "update sessions set void = 1 where sessid = %s"
        params = (sess_id,)
        result = sql_handler.put_query(query, params)
        if result is None:
            return error_codes.DB_ERROR
        else:
            return 0

    def get_session(session_id):
        query = "select * from sessions where sessid = %s and void = 0"
        params = (session_id,)
        result = sql_handler.put_query(query, params)
        if result is None or result == []:
            return error_codes.DB_ERROR
        else:
            return OrbitSession(*result[0])
