import uuid
import objects
from error_handler import ErrorCodes
from objects import Orbit
from dbhandler import sql_handler

error_codes = ErrorCodes()

class OrbitControl:

    def create_orbit(user_a, user_b, configuration):
        orb_id = str(uuid.uuid4())
        res0 = sql_handler.put_query("select user_a, user_b from Orbits")
        for i in res0:
            if user_a in i and user_b in i:
                return error_codes.ORBIT_ALREADY_EXISTS
        query = "insert into Orbits (orb_id, user_a, user_b, configuration) values (%s, %s, %s, %s)"
        params = (orb_id, user_a, user_b, configuration)
        result = sql_handler.put_query(query, params)
        if result is None:
            return error_codes.DB_ERROR
        else:
            return orb_id

    def get_orbit(orb_id):
        query = "select * from Orbits where orb_id = %s"
        params = (orb_id,)
        result = sql_handler.put_query(query, params)
        if result is None:
            return error_codes.DB_ERROR
        else:
            return Orbit(*result[0])

    def get_user_orbits(id):
        res = sql_handler.put_query("select * from orbits where user_a = %s or user_b = %s", (id, id))
        if res is None:
            return error_codes.DB_ERROR
        else:
            result = []
            for i in res:
                result.append(Orbit(*i))
            return result

    def get_orbit_bw_users(id1, id2):
        res = sql_handler.put_query("select * from orbits where (user_a = %s and user_b = %s) or (user_a = %s and user_b = %s)", (id1, id2, id2, id1))
        if res is None:
            return error_codes.DB_ERROR
        else:
            return Orbit(*res[0])

    def delete_orbit(orb_id):
        query = "delete from Orbits where orb_id = %s"
        params = (orb_id,)
        result = sql_handler.put_query(query, params)
        if result is None:
            return error_codes.DB_ERROR
        else:
            return 0

    def delete_orbit_messages(orb_id):
        query = "delete from OrbitMessages where orb_id = %s"
        params = (orb_id,)
        result = sql_handler.put_query(query, params)
        if result is None:
            return error_codes.DB_ERROR
        else:
            return 0

    def update_orbit(orb_id, user_a_msgs = None, user_b_msgs = None, G = None, M = None, I = None, user_a_last_response = None, user_b_last_response = None, configuration = None):
        query = "update Orbits set "
        params = []
        if user_a_msgs:
            query += "user_a_msgs = %s, "
            params.append(user_a_msgs)
        if user_b_msgs:
            query += "user_b_msgs = %s, "
            params.append(user_b_msgs)
        if G:
            query += "G = %s, "
            params.append(G)
        if M:
            query += "M = %s, "
            params.append(M)
        if I:
            query += "I = %s, "
            params.append(I)
        if user_a_last_response:
            query += "user_a_last_response = %s, "
            params.append(user_a_last_response)
        if user_b_last_response:
            query += "user_b_last_response = %s, "
            params.append(user_b_last_response)
        if configuration:
            query += "configuration = %s, "
            params.append(configuration)
        query = query.rstrip(", ")
        query += " where orb_id = %s"
        params.append(orb_id)
        result = sql_handler.put_query(query, params)
        if result is None:
            return error_codes.DB_ERROR
        else:
            return 0