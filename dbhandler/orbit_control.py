import uuid
import sql_handler

class OrbitControl:

    def create_orbit(IDa, IDb):
        orb_id = str(uuid.uuid4())
        query = "insert into Orbits (orb_id, user_a, user_b) values (%s, %s, %s)"
        params = (orb_id, IDa, IDb)
        result = sql_handler.put_query(query, params)
        if result is None:
            return 67
        else:
            return orb_id

    def get_orbit(orb_id):
        query = "select * from Orbits where orb_id = %s"
        params = (orb_id,)
        result = sql_handler.put_query(query, params)
        if result is None:
            return 67
        else:
            return result

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

    def update_orbit(orb_id, user_a_msgs, user_b_msgs, SNRNCOUNT, lastavg, G, M, I, user_a_last_response, user_b_last_response):
        query = "update Orbits set user_a_msgs = %s, user_b_msgs = %s, SNRNCOUNT = %s, lastavg = %s, G = %s, M = %s, I = %s, user_a_last_response = %s, user_b_last_response = %s where orb_id = %s"
        params = (user_a_msgs, user_b_msgs, SNRNCOUNT, lastavg, G, M, I, user_a_last_response, user_b_last_response, orb_id)
        result = sql_handler.put_query(query, params)
        if result is None:
            return 67
        else:
            return 0