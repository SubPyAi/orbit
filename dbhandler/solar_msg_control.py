import uuid
import objects
from error_handler import ErrorCodes
from objects import SolarMessage

from dbhandler import sql_handler
from dbhandler.solar_control import SolarControl

error_codes = ErrorCodes()

class SolarMsgControl:

    def add_message(sl_id, user_id, message, attributes):
        msg_id = str(uuid.uuid4())
        if SolarControl.is_solar_member(sl_id, user_id) == 1:
            query = "insert into SolarMessages (msg_id, sl_id, id, data, attributes) values (%s, %s, %s, %s, %s)"
            params = (msg_id, sl_id, user_id, message, attributes)
            result = sql_handler.put_query(query, params)
            if result is None:
                return error_codes.DB_ERROR
            else:
                return 0
        else:
            return error_codes.USER_NOT_SOLAR_MEMBER

    def update_message(id, msg_id, message):
        print(sql_handler.put_query("select id from solarmessages where msg_id = %s", (msg_id,))[0][0])
        if str(id) != (sql_handler.put_query("select id from solarmessages where msg_id = %s", (msg_id,))[0][0]):
            return error_codes.UNAUTHORISED_REQUEST
        query = "update SolarMessages set data = %s, edited = edited + 1 where msg_id = %s"
        params = (message, msg_id)
        result = sql_handler.put_query(query, params)
        if result is None:
            return error_codes.DB_ERROR
        else:
            return 0

    def get_messages(sl_id, id, offset=0, limit=100):
        if SolarControl.is_solar_member(sl_id, id) == 1:
            query = "select * from SolarMessages where sl_id = %s order by at desc limit %s offset %s"
            params = (sl_id, limit, offset)
            result = sql_handler.put_query(query, params)
            if result is None:
                return error_codes.DB_ERROR
            else:
                list_messages = []
                for message_data in result:
                    list_messages.append(SolarMessage(*message_data))
                return list_messages
        else:
            return error_codes.UNAUTHORISED_REQUEST

    def delete_message(msg_id, id):
        req = sql_handler.put_query("select id from solarmessages where msg_id = %s", (msg_id,))
        if req == []:
            return error_codes.MESSAGE_DOES_NOT_EXIST
        if id != req[0][0]:
            return error_codes.UNAUTHORISED_REQUEST
        query = "delete from SolarMessages where msg_id = %s"
        params = (msg_id,)
        result = sql_handler.put_query(query, params)
        if result is None:
            return error_codes.DB_ERROR
        else:
            return 0

    def get_message(msg_id):
        query = "select * from SolarMessages where msg_id = %s"
        params = (msg_id,)
        result = sql_handler.put_query(query, params)
        if result is None:
            return error_codes.DB_ERROR
        else:
            return SolarMessage(*result[0])