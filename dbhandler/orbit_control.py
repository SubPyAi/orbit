import uuid
import objects
from objects import Orbit
from dbhandler import sql_handler

class OrbitControl:

    def create_orbit(orb: Orbit):
        orb.orb_id = str(uuid.uuid4())
        query = "insert into Orbits (orb_id, user_a, user_b, configuration) values (%s, %s, %s, %s)"
        params = (orb.orb_id, orb.user_a, orb.user_b, orb.configuration)
        result = sql_handler.put_query(query, params)
        if result is None:
            return 67
        else:
            return orb.orb_id

    def get_orbit(orb_id):
        query = "select * from Orbits where orb_id = %s"
        params = (orb_id,)
        result = sql_handler.put_query(query, params)
        if result is None:
            return 67
        else:
            return Orbit(*result[0])

    def delete_orbit(orb_id):
        query = "delete from Orbits where orb_id = %s"
        params = (orb_id,)
        result = sql_handler.put_query(query, params)
        if result is None:
            return 67
        else:
            return 0

    def delete_orbit_messages(orb_id):
        query = "delete from OrbitMessages where orb_id = %s"
        params = (orb_id,)
        result = sql_handler.put_query(query, params)
        if result is None:
            return 67
        else:
            return 0

    def update_orbit(orb_id, user_a_msgs = None, user_b_msgs = None, G = None, M = None, I = None, user_a_last_response = None, user_b_last_response = None):
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
        query = query.rstrip(", ")
        query += " where orb_id = %s"
        params.append(orb_id)
        result = sql_handler.put_query(query, params)
        if result is None:
            return 67
        else:
            return 0