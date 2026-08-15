import uuid
import datetime
from dbhandler import sql_handler

class SessionControl:

    def create_session(user_id):
        sess_id = str(uuid.uuid4())
        created = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        query = "insert into sessions (sessid, id, created) values (%s, %s, %s)"
        params = (sess_id, user_id, created)
        result = sql_handler.put_query(query, params)
        if result is None:
            return 67
        else:
            return 0

    def validate_session(sess_id):
        query = "select void from sessions where sessid = %s"
        params = (sess_id,)
        result = sql_handler.put_query(query, params)
        if result is None:
            return 67
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
            return 67
        else:
            return 0

    def get_session(sess_id):
        query = "select * from sessions where sessid = %s"
        params = (sess_id,)
        result = sql_handler.put_query(query, params)
        if result is None:
            return 67
        else:
            return result
