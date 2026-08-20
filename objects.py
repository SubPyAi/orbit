from fastapi import WebSocket

class User:
    def __init__(self, id, username, password, email, phone, DoB, created, pfp_ref, online):
        self.id = id
        self.username = username
        self.password = password
        self.email = email
        self.phone = phone
        self.DoB = DoB
        self.created = created
        self.pfp_ref = pfp_ref
        self.online = online


class Solar:
    def __init__(self, sl_id, id, name, configuration, created, msgdata):
        self.sl_id = sl_id
        self.id = id
        self.name = name
        self.configuration = configuration
        self.created = created
        self.msgdata = msgdata


class OrbitSession:
    def __init__(self, sessid, id, created, void):
        self.sessid = sessid
        self.id = id
        self.created = created
        self.void = void


class Orbit:
    def __init__(self, orb_id, user_a, user_b, user_a_msgs, user_b_msgs, last_var_assignment, G, M, I, user_a_last_response, user_b_last_response, configuration):
        self.orb_id = orb_id
        self.user_a = user_a
        self.user_b = user_b
        self.user_a_msgs = user_a_msgs
        self.user_b_msgs = user_b_msgs
        self.last_var_assignment = last_var_assignment
        self.G = G
        self.M = M
        self.I = I
        self.user_a_last_response = user_a_last_response
        self.user_b_last_response = user_b_last_response
        self.configuration = configuration


class SolarMember:
    def __init__(self, sl_id, id, joined, attributes):
        self.sl_id = sl_id
        self.id = id
        self.joined = joined
        self.attributes = attributes


class OrbitMessage:
    def __init__(self, msg_id, orb_id, id, data, at, edited, attributes):
        self.msg_id = msg_id
        self.orb_id = orb_id
        self.id = id
        self.data = data
        self.at = at
        self.edited = edited
        self.attributes = attributes


class SolarMessage:
    def __init__(self, msg_id, sl_id, id, data, at, edited, attributes):
        self.msg_id = msg_id
        self.sl_id = sl_id
        self.id = id
        self.data = data
        self.at = at
        self.edited = edited
        self.attributes = attributes

class ActiveWSConnection:
    def __init__(self, ws: WebSocket, id, void):
        self.ws = ws
        self.id = id
        self.void = void