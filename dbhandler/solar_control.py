import uuid
import datetime
import json
import itertools
import objects
from objects import Solar
from dbhandler import sql_handler
from dbhandler.user_control import UserControl

class SolarControl:

    def create_solar(user_id, name, conf):
        sl_id = str(uuid.uuid4())
        if UserControl.get_user(user_id) == 1:
            return 1
        print(conf)
        cfg = json.loads(conf)
        msgdata = {"member_data": {}, "last_var_assignment": "", "member_variables": {}}
        for i in cfg['members']:
            msgdata["member_data"][i] = 0
        msgdata["last_var_assignment"] = datetime.date.today().strftime("%d-%m-%Y")
        pairs = itertools.combinations(cfg['members'], 2)
        for i in pairs:
            msgdata['member_variables'][i[0] + ":" + i[1]] = 0
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
            return Solar(*request[0])

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

    def add_role(sl_id, role, permissions):
        request = sql_handler.put_query("select configuration from Solars where sl_id = %s", (sl_id,))
        if request is None:
            return 67

        config = json.loads(request[0][0])
        if role in config['roles']:
            return 1

        config['roles'][role] = permissions
        config['role_map'][role] = []
        request = sql_handler.put_query("update Solars set configuration = %s where sl_id = %s", (json.dumps(config), sl_id))
        if request is None:
            return 67
        else:
            return 0

    def remove_role(sl_id, role):
        request = sql_handler.put_query("select configuration from Solars where sl_id = %s", (sl_id,))
        if request is None:
            return 67

        config = json.loads(request[0][0])

        if config['role_map'][role] != []:
            return 2

        if role not in config['roles']:
            return 1

        del config['roles'][role]
        config['role_map'].pop(role, None)
        request = sql_handler.put_query("update Solars set configuration = %s where sl_id = %s", (json.dumps(config), sl_id))
        if request is None:
            return 67
        else:
            return 0

    def assign_role(sl_id, id, role):
        request = sql_handler.put_query("select configuration from Solars where sl_id = %s", (sl_id,))
        if request is None:
            return 67

        config = json.loads(request[0][0])
        if role not in config['roles']:
            return 1

        if id not in config['members']:
            return 2

        for assigned_role in config['role_map']:
            if id in config['role_map'][assigned_role]:
                config['role_map'][assigned_role].remove(id)

        config['role_map'].setdefault(role, []).append(id)
        request = sql_handler.put_query("update Solars set configuration = %s where sl_id = %s", (json.dumps(config), sl_id))
        if request is None:
            return 67
        else:
            return 0

    def add_member(sl_id, id, uname, role):
        request1 = sql_handler.put_query("select configuration, msgdata from Solars where sl_id = %s", (sl_id,))
        if request1 is None:
            return 67

        config = json.loads(request1[0][0])

        if id in config['ban_list']:
            return 1

        if id in config['members']:
            return 2

        if len(config['members']) == int(config['max_mambers']):
            return 3
        
        mem_list = config['members']

        config['members'][id] = uname

        msgdata = json.loads(request1[0][1])
        for i in mem_list:
            msgdata['member_variables'][id + ":" + i] = 0

        msgdata['member_data'][id] = 0

        config['role_map'][role].append(id)
        

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

        del msgdata['member_data'][id]

        for i in config['members'].keys():
            del msgdata['member_variables'][id + ":" + i]

        for i in config['roles'].keys():
            if id in config['role_map'][i]:
                config['role_map'][i].remove(id)

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

    def get_solars(id):
        response = []
        req1 = sql_handler.put_query("select * from solars;")
        for i in req1:
            conf = json.loads(i[3])
            if id in conf['members']:
                response.append(Solar(*i))
        return response

    def get_user_permissions(sl_id, id):
        req = sql_handler.put_query("select * from solars where sl_id = %s", (sl_id,))
        res = set()
        conf = json.loads(req[3])
        for i in conf['roles'].keys():
            if id in conf['role_map'][i]:
                for j in conf['roles'][i]:
                    res.add(j)
        return list(res)

