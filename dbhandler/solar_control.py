import uuid
import datetime
import json
import itertools
from dbhandler import sql_handler
from dbhandler.user_control import UserControl

class SolarControl:

    def create_solar(user_id, name, conf):
        sl_id = str(uuid.uuid4())
        cfg = json.loads(conf)
        msgdata = {"member_data": {}, "last_var_assignment": "", "member_variables": {}}
        for i in cfg['members']:
            msgdata["member_variables"][i] = 0
        msgdata["last_var_assignment"] = datetime.date.today().strftime("%d-%m-%Y")
        pairs = itertools.combinations(cfg['members'], 2)
        for i in pairs:
            msgdata['member_data'][i[0] + ":" + i[1]] = 0
        query = "insert into Solars (sl_id, name, id, configuration, msgdata) values (%s, %s, %s, %s, %s)"
        params = (sl_id, name, user_id, conf, json.dumps(msgdata))
        print(query % params)
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

    def update_solar(sl_id, name=None, configuration=None):
        query = 'update Solars set '
        params = []
        if name:
            query += 'name = %s, '
            params.append(name)
        if configuration:
            query += 'configuration = %s '
            params.append(configuration)

        query = query.rstrip(', ')
        query += " where sl_id = %s"
        params.append(sl_id)
        request = sql_handler.put_query(query, params)
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

    def add_member(sl_id, id, uname):
        request1 = sql_handler.put_query("select configuration, msgdata from Solars where sl_id = %s", (sl_id,))
        if request1 is None:
            return 67

        config = json.loads(request1[0][0])

        if id in config['ban_list']:
            return 1

        if id in config['members']:
            return 2
        
        mem_list = config['members']
        for i in mem_list:
            msgdata['member_data'][id + ":" + i] = 0

        config['members'][id] = uname

        msgdata = json.loads(request1[0][1])
        for i in mem_list:
            msgdata['member_variables'][id] = 0
        

        request = sql_handler.put_query("update Solars set configuration = %s, msgdata = %s where sl_id = %s", (json.dumps(config), json.dumps(msgdata), sl_id))

        return 0

    def remove_member(sl_id, id):
        request1 = sql_handler.put_query("select configuration, msgdata from Solars where sl_id = %s", (sl_id,))
        if request1 is None:
            return 67

        config = json.loads(request1[0][0])

        if id not in config['members']:
            return 1

        del config['members'][id]
        msgdata = json.loads(request1[0][1])

        del msgdata['member_variables'][id]

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
    

