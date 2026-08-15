import uuid
import json
from dbhandler import sql_handler

class SolarControl:

    def create_solar(user_id, name, conf):
        sl_id = str(uuid.uuid4())
        cfg = json.loads(conf)
        msgdata = []
        for i in cfg['members']:
            msgdata.append({i: 0})
        query = "insert into Solars (sl_id, name, id, configuration, msgdata) values (%s, %s, %s, %s, %s)"
        params = (sl_id, name, user_id, conf, msgdata)
        request = sql_handler.put_query(query, params)
        if request == None:
            return 67
        else:
            return sl_id

    def delete_solar(sl_id):
        request = sql_handler.put_query("delete from Solars where sl_id is %s", (sl_id,))
        if request == None:
            return 67
        else:
            return 0

    def get_solar(sl_id):
        request = sql_handler.put_query("select * from Solars where sl_id is %s", (sl_id,))
        if request == None:
            return 67
        elif request == []:
            return 1
        else:
            return request

    def update_solar(sl_id, name, configuration):
        request = sql_handler.put_query("update Solars set name = %s, configuration = %s where sl_id = %s", (name, configuration, sl_id))
        if request == None:
            return 67
        else:
            return 0