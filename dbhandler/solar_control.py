import uuid
import datetime
import json
import itertools
from dbhandler import sql_handler

class SolarControl:

    def create_solar(user_id, name, conf):
        sl_id = str(uuid.uuid4())
        cfg = json.loads(conf)
        msgdata = {"member_data": {}, "last_var_assignment": "", "member_data": {}}
        for i in cfg['members']:
            msgdata["member_data"][i] = 0
        msgdata["last_var_assignment"] = datetime.date.today().strftime("%d-%m-%Y")
        pairs = itertools.combination(cfg['members'], 2)
        for i in pairs:
            msgdata['member_data'][i[0] + ":" + i[1]] = 0
        query = "insert into Solars (sl_id, name, id, configuration, msgdata) values (%s, %s, %s, %s, %s)"
        params = (sl_id, name, user_id, conf, json.dumps(msgdata))
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
        request = sql_handler.put_query("select * from Solars where sl_id = %s", (sl_id,))
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

    def update_solar_msg_data(sl_id, msgdata):
        request = sql_handler.put_query("update Solars set msgdata = %s where sl_id = %s", (msgdata, sl_id))
        if request == None:
            return 67
        else:
            return 0

    def add_member(sl_id, id):
        request1 = sql_handler.put_query("select configuration from Solars where sl_id is %s", (sl_id,))
        if request1 is None:
            return 67

        config = json.loads(request1[0][3])

        if id in config['ban_list']:
            return 1

        mem_list = config['members']
        config['members']['id'] = 0

        msgdata = json.loads(request1[0][5])
        msgdata['member_data'][id] = 0
        for i in mem_list:
            msgdata['member_variables'][i + ':' + id] = 0
        

        request = sql_handler.put_query("update Solars set configuration = %s, msgdata = %s where sl_id = %s", (config, msgdata, sl_id))

        return 0

    def remove_member(sl_id, id):
        request1 = sql_handler.put_query("select configuration from Solars where sl_id is %s", (sl_id,))
        if request1 is None:
            return 67

        config = json.loads(request1[0][3])

        if id not in config['members']:
            return 1

        config['members'].remove(id)
        msgdata = json.loads(request1[0][5])

        if id in msgdata['member_data']:
            del msgdata['member_data'][id]

        for key in list(msgdata['member_data'].keys()):
            if id in key:
                del msgdata['member_data'][key]

        request = sql_handler.put_query("update Solars set configuration = %s, msgdata = %s where sl_id = %s", (json.dumps(config), json.dumps(msgdata), sl_id))
        if request is None:
            return 67
        else:
            return 0

    def ban_member(sl_id, id):
        request1 = sql_handler.put_query("select configuration from Solars where sl_id is %s", (sl_id,))
        if request1 is None:
            return 67

        config = json.loads(request1[0][3])

        if id in config['ban_list']:
            return 1

        config['ban_list'].append(id)

        request = sql_handler.put_query("update Solars set configuration = %s where sl_id = %s", (json.dumps(config), sl_id))
        if request is None:
            return 67
        else:
            return 0

    def unban_member(sl_id, id):
        request1 = sql_handler.put_query("select configuration from Solars where sl_id is %s", (sl_id,))
        if request1 is None:
            return 67

        config = json.loads(request1[0][3])

        if id not in config['ban_list']:
            return 1

        config['ban_list'].remove(id)

        request = sql_handler.put_query("update Solars set configuration = %s where sl_id = %s", (json.dumps(config), sl_id))
        if request is None:
            return 67
        else:
            return 0

