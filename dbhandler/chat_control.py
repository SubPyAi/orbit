import uuid
from dbhandler import sql_handler

class ChatControl:

    def add_message(orb_id, user_id, message):
        msg_id = str(uuid.uuid4())
        query = "insert into OrbitMessages (msg_id, orb_id, id, data) values (%s, %s, %s, %s)"
        params = (msg_id, orb_id, user_id, message)
        result = sql_handler.put_query(query, params)
        if result is None:
            return 67
        else:
            return 0

    def update_message(msg_id, message):
        query = "update OrbitMessages set data = %s, edited = edited + 1 where msg_id = %s"
        params = (message, msg_id)
        result = sql_handler.put_query(query, params)
        if result is None:
            return 67
        else:
            return 0

    def get_messages(orb_id, offset=0, limit=100):
        query = "select * from OrbitMessages where orb_id = %s order by at limit %s offset %s"
        params = (orb_id, limit, offset)
        result = sql_handler.put_query(query, params)
        if result is None:
            return 67
        else:
            return result

    def delete_message(msg_id):
        query = "delete from OrbitMessages where msg_id = %s"
        params = (msg_id,)
        result = sql_handler.put_query(query, params)
        if result is None:
            return 67
        else:
            return 0

    def get_message(msg_id):
        query = "select * from OrbitMessages where msg_id = %s"
        params = (msg_id,)
        result = sql_handler.put_query(query, params)
        if result is None:
            return 67
        else:
            return result