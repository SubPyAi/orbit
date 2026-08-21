import json

from ws_events import WSEvents

from api_model import WSRecv

from error_handler import OrbitException
from error_handler import ErrorCodes

from dbhandler.chat_control import ChatControl
from dbhandler.orbit_control import OrbitControl
from dbhandler.solar_control import SolarControl
from dbhandler.solar_msg_control import SolarMsgControl

wsevents = WSEvents()
error_codes = ErrorCodes()

def validate_res(err_code):
    if err_code in vars(error_codes).values():
        return err_code
    return None

class WSHandler:

    def __init__(self, content: WSRecv):
        self.event = content.event
        self.data = content.data
        self.id = str(content.id)
        self.update_event = {}

    def process(self):
        try:
            if self.event == wsevents.WS_CLIENT_ADD_ORBIT_MESSAGE:
                res = ChatControl.add_message(self.data['orb_id'], self.id, self.data['message'], self.data['attributes'])
                self.update_event['event'] = wsevents.WS_SERVER_UPDATE_ORBIT_MESSAGE
                self.update_event['primary_spec_id'] = self.data['orb_id']
                self.update_event['secondary_spec_id'] = None
                return (validate_res(res) if validate_res(res) else 0)
            elif self.event == wsevents.WS_CLIENT_EDIT_ORBIT_MESSAGE:
                res = ChatControl.update_message(self.data['msg_id'], self.data['msg'])
                self.update_event['event'] = wsevents.WS_SERVER_UPDATE_ORBIT_MESSAGE
                self.update_event['primary_spec_id'] = self.data['orb_id']
                self.update_event['secondary_spec_id'] = self.data['msg_id']
                return (validate_res(res) if validate_res(res) else 0)
            elif self.event == wsevents.WS_CLIENT_DELETE_ORBIT_MESSAGE:
                res = ChatControl.delete_message(self.data['msg_id'])
                self.update_event['event'] = wsevents.WS_SERVER_UPDATE_ORBIT_DELETE_MESSAGE
                self.update_event['primary_spec_id'] = self.data['orb_id']
                self.update_event['secondary_spec_id'] = self.data['msg_id']
                return (validate_res(res) if validate_res(res) else 0)
            elif self.event == wsevents.WS_CLIENT_MODIFY_ORBIT_USER_COLOR:
                res = OrbitControl.update_orbit_user_color(self.data['orb_id'], self.id, self.data['col'])
                self.update_event['event'] = wsevents.WS_SERVER_UPDATE_ORBIT
                self.update_event['primary_spec_id'] = self.data['orb_id']
                self.update_event['secondary_spec_id'] = None
                return (validate_res(res) if validate_res(res) else 0)
            elif self.event == wsevents.WS_CLIENT_ADD_SOLAR_MESSAGE:
                req = SolarControl.get_solar_config(self.data['sl_id'])
                if validate_res(req):
                    return validate_res(req)
                if req['allow_media'] == 0 and (json.loads(self.data['attributes']))['is_media'] == 1:
                    return validate_res(error_codes.MEDIA_NOT_ALLOWED_IN_SOLAR)
                res = SolarMsgControl.add_message(self.data['sl_id'], self.id, self.data['message'], self.data['attributes'])
                self.update_event['event'] = wsevents.WS_SERVER_UPDATE_SOLAR_MESSAGE
                self.update_event['primary_spec_id'] = self.data['sl_id']
                self.update_event['secondary_spec_id'] = None
                return (validate_res(res) if validate_res(res) else 0)
            elif self.event == wsevents.WS_CLIENT_EDIT_SOLAR_MESSAGE:
                req = SolarControl.get_solar_config(self.data['sl_id'])
                if validate_res(req):
                    return validate_res(req)
                if req['allow_edit'] == 0:
                    return validate_res(error_codes.DELETION_NOT_ALLOWED_IN_SOLAR)
                res = SolarMsgControl.update_message(self.data['msg_id'], self.data['msg'])
                self.update_event['event'] = wsevents.WS_SERVER_UPDATE_SOLAR_MESSAGE
                self.update_event['primary_spec_id'] = self.data['sl_id']
                self.update_event['secondary_spec_id'] = self.data['msg_id']
                return (validate_res(res) if validate_res(res) else 0)
            elif self.event == wsevents.WS_CLIENT_DELETE_SOLAR_MESSAGE:
                req = SolarControl.get_solar_config(self.data['sl_id'])
                if validate_res(req):
                    return validate_res(req)
                if req['allow_delete'] == 0:
                    return validate_res(error_codes.DELETION_NOT_ALLOWED_IN_SOLAR)
                res = SolarControl.delete_message(self.data['msg_id'])
                self.update_event['event'] = wsevents.WS_SERVER_UPDATE_SOLAR_DELETE_MESSAGE
                self.update_event['primary_spec_id'] = self.data['sl_id']
                self.update_event['secondary_spec_id'] = self.data['msg_id']
                return (validate_res(res) if validate_res(res) else 0)
            elif self.event == wsevents.WS_CLIENT_MODIFY_SOLAR_USER_COLOR:
                res = SolarControl.set_user_col(self.data['sl_id'], self.id, self.data['col'])
                self.update_event['event'] = wsevents.WS_SERVER_UPDATE_SOLAR
                self.update_event['primary_spec_id'] = self.data['sl_id']
                self.update_event['secondary_spec_id'] = None
                return (validate_res(res) if validate_res(res) else 0)
        except:
            validate_res(error_codes.INVALID_INPUT_FORMAT)
