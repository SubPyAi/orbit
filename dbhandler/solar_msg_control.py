import uuid
from dbhandler import sql_handler

class SolarMsgControl:

    def add_message(sl_id, user_id, message):
        msg_id = str(uuid.uuid4())
        query = "insert into SolarMessages (msg_id, sl_id, id, data) values (%s, %s, %s, %s)"
        params = (msg_id, sl_id, user_id, message)
        result = sql_handler.put_query(query, params)
        if result is None:
            return 67
        else:
            return 0

    def update_message(msg_id, message):
        query = "update SolarMessages set data = %s, edited = edited + 1 where msg_id = %s"
        params = (message, msg_id)
        result = sql_handler.put_query(query, params)
        if result is None:
            return 67
        else:
            return 0

    def get_messages(sl_id, offset=0, limit=100):
        query = "select * from SolarMessages where sl_id = %s order by at desc limit %s offset %s"
        params = (sl_id, limit, offset)
        result = sql_handler.put_query(query, params)
        if result is None:
            return 67
        else:
            return result

    def delete_message(msg_id):
        query = "delete from SolarMessages where msg_id = %s"
        params = (msg_id,)
        result = sql_handler.put_query(query, params)
        if result is None:
            return 67
        else:
            return 0

    def get_message(msg_id):
        query = "select * from SolarMessages where msg_id = %s"
        params = (msg_id,)
        result = sql_handler.put_query(query, params)
        if result is None:
            return 67
        else:
            return result