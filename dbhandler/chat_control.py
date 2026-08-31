import uuid
import objects

from error_handler import ErrorCodes
from objects import OrbitMessage
from dbhandler import sql_handler
from dbhandler.orbit_control import OrbitControl

error_codes = ErrorCodes()

class ChatControl:

    def add_message(orb_id, user_id, message, attributes):
        msg_id = str(uuid.uuid4())
        res = OrbitControl.is_user_in_orbit(orb_id, user_id)
        if not res:
            return error_codes.UNAUTHORISED_REQUEST
        query = "insert into OrbitMessages (msg_id, orb_id, id, data, attributes) values (%s, %s, %s, %s, %s)"
        params = (msg_id, orb_id, user_id, message, attributes)
        result = sql_handler.put_query(query, params)
        if result is None:
            return error_codes.DB_ERROR
        else:
            return 0

    def update_message(user_id, msg_id, orb_id, message):
        req = OrbitControl.is_user_in_orbit(orb_id, user_id)
        if req == False:
            return error_codes.UNAUTHORISED_REQUEST
        query = "update OrbitMessages set data = %s, edited = edited + 1 where msg_id = %s and orb_id = %s"
        params = (message, msg_id, orb_id)
        result = sql_handler.put_query(query, params)
        if result is None:
            return error_codes.DB_ERROR
        else:
            return 0

    def get_messages(orb_id, offset=0, limit=100):
        query = "select * from OrbitMessages where orb_id = %s order by at limit %s offset %s"
        params = (orb_id, limit, offset)
        result = sql_handler.put_query(query, params)
        if result is None:
            return error_codes.DB_ERROR
        else:
            list_messages = []
            for message_data in result:
                list_messages.append(OrbitMessage(*message_data))
            return list_messages

    def delete_message(user_id, orb_id, msg_id):
        req = OrbitControl.is_user_in_orbit(orb_id, user_id)
        if req == False:
            return error_codes.UNAUTHORISED_REQUEST
        query = "delete from OrbitMessages where msg_id = %s and orb_id = %s"
        params = (msg_id, orb_id)
        result = sql_handler.put_query(query, params)
        if result is None:
            return error_codes.DB_ERROR
        else:
            return 0

    def get_message(msg_id):
        query = "select * from OrbitMessages where msg_id = %s"
        params = (msg_id,)
        result = sql_handler.put_query(query, params)
        if result is None:
            return error_codes.DB_ERROR
        else:
            return OrbitMessage(*result[0])