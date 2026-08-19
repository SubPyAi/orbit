import json
import fastapi
import secrets
import api_model
import dbhandler

from dbhandler import UserControl
from dbhandler import OrbitControl
from dbhandler import SolarControl
from dbhandler import SolarMsgControl
from dbhandler import ChatControl
from dbhandler import SessionControl
from dbhandler import VerificationControl

from fastapi import Request
from fastapi.responses import JSONResponse

#initialise fastapi app
app = fastapi.FastAPI()


#
# Orbit API v1
#

# LOGIN AUTHENTICATION FUNCTIONS

@app.post('/api/v1/auth/login')
def login(username: str = None, password: str = None, session: str = None):
    if username and password:
        result1 = UserControl.validate_user(username, password)
        if result1 == 0:
            result2 = SessionControl.create_session(UserControl.get_uid(username))
            response = JSONResponse({"status": 0, "auth_status": 0})
            if result2 == 67:
                return {"status": 2, "Error": "internal server error"}
            else:
                response.set_cookie(
                    key = "session",
                    value = result2,
                    httponly = True,
                    secure = True,
                    samesite = "lax", 
                    path = "/"
                )
                return response
    elif session:
        result = SessionControl.validate_session(session)
        if result == 67:
            return {"status": 2, "Error": "Internal database error"}
        else:
            if result:
                return {"status": 0, "auth_status": 0}
            else:
                return {"status": 0, "auth_status": 1}

    else:
        return {"status": 2, "Error": "Unexpeced input error."}

@app.post('/api/v1/auth/logout')
def logout(request: Request):
    sessionid = request.cookies.get('session')
    if not sessionid:
        pass
    result = SessionControl.revoke_session(sessionid)
    if result == 67:
        return {"status": 2, "Error": "Internal database error"}
    else:
        response = JSONResponse({"auth_status": 1})
        response.delete_cookie(key = "session")
        return response

@app.get('/api/v1/auth/me')
def get_current_user(request: Request):
    sess_id = request.cookies.get("session")
    if sess_id:
        req = SessionControl.validate_session(sess_id)
        if req == 67:
            return {"status": 2, "Error": "Internal database error"}
        else:
            session = SessionControl.get_session(sess_id)
            return {"status": 0, "uid": session.id}
    else:
        return {"status": 1, "Warning": "session_token_null"}


# SIGN UP AUTHENTICATION FUNCTIONS

@app.post('/api/v1/signup/create')
def create_new_user(username: str = None, password: str = None, email: str = None, phone: str = None, DoB: str = None, pfp_ref: str = None):
    if not (username or password or email or phone or DoB):
        return {"Error": "Invalid POST request!"}
    else:
        result = UserControl.create_user(username, password, email, phone, DoB, pfp_ref)
        if result == 67:
            return {"status": 2, "Error": "Internal databse error"}
        elif result == 1:
            return {"status": 0, "account_creation": "failure"}
        else:
            return {"status": 0, "account_creation": "success"}

# GENERAL LEVEL USER QUERY FUNCTIONS

@app.get('/api/v1/users/get')
def get_user(uname: str = None, uid: str = None):
    if uname:
        user =  UserControl.get_user(UserControl.get_uid(uname))
        if user == 67:
            return {"status": 2, "Error": "Internal database error"}
        elif user == 1:
            return {"status": 1, "Warning": "Invalid username"}
        else:
            return {"status": 0, "username": user.username, "DoB": user.DoB, "created": user.created, "pfp_ref": user.pfp_ref}
    elif uid:
        user =  UserControl.get_user(uid)
        if user == 67:
            return {"status": 2, "Error": "Internal database error"}
        elif user == 1:
            return {"status": 1, "Warning": "Invalid username"}
        else:
            return {"status": 0, "username": user.username, "DoB": user.DoB, "created": user.created, "pfp_ref": user.pfp_ref}
    else:
        return {"status": 2, "Error": "Invalid request!"}


# USER VERIFICATION FUNCTIONS

def send_new_verification_email(id, email):
    return VerificationControl.add_new_verification(id, email, "".join([str(secrets.randbelow(10)) for _ in range(6)]), 'email')

def verify_token(id, token):
    return VerificationControl.validate_token(id, token)
        
# USER LEVEL ACCOUNT MODIFICATION FUNCTIONS

@app.patch('/api/v1/users/modify')
def modify_user(params: str, request: Request):
    sessid = request.cookies.get("session")
    if sessid:
        result = SessionControl.validate_session(sessid)
        params = json.loads(params)
        if result == 67:
            return {"status": 2, "Error": "Internal database error"}
        else:
            if result:
                session = SessionControl.get_session(sessid)
                user = UserControl.get_user(session.id)
                res = UserControl.update_user(user.id, params.get('username'), None, None, None, params.get('DoB'), params.get('pfp_ref'))
                if res == 67:
                    return {"status": 2, "Error": "Internal database error"}
                else:
                    return {"status": 0}
            else:
                response = JSONResponse({"status": 0, "auth_status": 1})
                response.delete_cookie('session')
                return response
    else:
        return {"status": 3, "AuthError": "Unauthorised request"}

# SOLAR CRUD

@app.post('/api/v1/solars/create')
def create_solar(params: str, request: Request):
    params = json.loads(params)
    session = SessionControl.get_session(request.cookies.get('session'))
    if session != 67:
        res = SolarControl.create_solar(session.id, params['name'], json.dumps(params['configuration']))
        if res == 67:
            return {"status": 2, "Error": "Internal database error"}
        elif res == 1:
            return {"status": 1, "Error": "Invalid Session token"}
        else:
            return {"status": 0, "sl_id": res}
    else:
        return {"status": 2, "Error": "Internal database error"}

@app.get('/api/v1/solars/get/{sl_id}')
def get_solar(sl_id: str):
    solar = SolarControl.get_solar(sl_id)
    if solar == 67:
        return {"status": 2, "Error": "Internal database error"}
    elif solar == 1:
        return {"status": 1, "Error": "Invalid Solar ID"}
    else:
        return {"status": 0, "sl_id": solar.sl_id, "id": solar.id, "name": solar.name, "configuration": solar.configuration, "created": solar.created}

@app.get('/api/v1/solars/mysolars')
def get_user_solars(request: Request):
    session = SessionControl.get_session(request.cookies.get('session'))
    if session == 67:
        return {"status": 2, "Error": "Internal database error"}
    else:
        solars = SolarControl.get_solars(session.id)
        return {"status": 0, "solars": solars}

@app.post('/api/v1/solars/{sl_id}/leave')
def leave_solar(sl_id: str, request: Request):
    session = SessionControl.get_session(request.cookies.get('session'))
    if session == 67:
        return {"status": 1, "AuthError": "Unauthorised request"}

    result = SolarControl.remove_member(sl_id, session.id)
    if result == 67:
        return {"status": 2, "Error": "Internal database error"}
    elif result == 1:
        return {"status": 1, "Error": "User is not a member!"}
    else:
        return {"status": 0}

@app.patch('/api/v1/solars/{sl_id}/modify/{key}')
def modify_solar(sl_id: str, key: str, value, action, request: Request):
    session = SessionControl.get_session(request.cookies.get('session'))
    perms = SolarControl.get_user_permissions(sl_id, session.id)
    if key == 'members':
        if "manage_members" in perms:
            # value must be of type [{"id": id, "uname": uname, "role": []}, ...]
            if action == 'add':
                for i in value:
                    res = SolarControl.add_member(sl_id, i['id'], i['uname'], i['role'])
                    if res == 67:
                        return {"status": 2, "Error": "Internal database error"}
                    else:
                        pass
                return {"status": 0}
            elif action == 'remove':
                for i in value:
                    res = SolarControl.remove_member(sl_id, i['id'])
                    if res == 67:
                        return {"status": 2, "Error": "Internal database error"}
                    else:
                        pass
                return {"status": 0}
            elif action == 'ban':
                for i in value:
                    res = SolarControl.remove_member(sl_id, i['id'])
                    SolarControl.ban_member(sl_id, i['id'])
                    if res == 67:
                        return {"status": 2, "Error": "Internal database error"}
                    else:
                        pass
                return {"status": 0}
            elif action == 'unban':
                for i in value:
                    res = SolarControl.unban_member(sl_id, i['id'])
                    if res == 67:
                        return {"status": 2, "Error": "Internal database error"}
                    else:
                        pass
                return {"status": 0}
            else:
                return {"status": 1, "InvalidInput": "Invalid request!"}
        else:
            return {"status": 1, "PermsError": "Insufficient permissions!"}
    elif key == 'roles':
        if "manage_roles" in perms:
            if action == 'add':
                for i in value:
                    res = SolarControl.add_role(sl_id, i['role'], i['perms'])
                    if res == 67:
                        return {"status": 2, "Error": "Internal database error"}
                    elif res == 1:
                        return {"status": 1, "Error": "Role already exists!"}
                    else:
                        pass
                return {"status": 0}
            elif action == 'remove':
                for i in value:
                    res = SolarControl.remove_role(sl_id, i['role'])
                    if res == 67:
                        return {"status": 2, "Error": "Internal database error"}
                    elif res == 2:
                        return {"status": 1, "Error": "Role not empty!"}
                    elif res == 1:
                        return {"status": 1, "Error": "Role not found!"}
                    else:
                        return {"status": 0}
            elif action == 'assign':
                for i in value:
                    res = SolarControl.assign_role(sl_id, i['id'], i['role'])
                    if res == 67:
                        return {"status": 2, "Error": "Internal database error"}
                    elif res == 1:
                        return {"status": 1, "Error": "Role not found!"}
                    elif res == 2:
                        return {"status": 1, "Error": "User is not a member!"}
                    else:
                        pass
            else:
                return {"status": 1, "InvalidInput": "Invalid request!"}
        else:
            return {"status": 1, "PermsError": "Insufficient permissions!"}
    elif key == 'config':
        if "manage_config" not in perms:
            return {"status": 1, "PermsError": "Insufficient permissions!"}

        if action not in ('update', 'set'):
            return {"status": 1, "InvalidInput": "Invalid request!"}

        if isinstance(value, str):
            try:
                value = json.loads(value)
            except json.JSONDecodeError:
                return {"status": 1, "InvalidInput": "Configuration must be valid JSON!"}

        if not isinstance(value, dict):
            return {"status": 1, "InvalidInput": "Configuration must be a JSON object!"}

        res = SolarControl.update_solar(sl_id, configuration=json.dumps(value))
        if res == 67:
            return {"status": 2, "Error": "Internal database error"}
        else:
            return {"status": 0}
    else:
        return {"status": 1, "InvalidInput": "Invalid request!"}
                    
@app.get('/')
def root():
    return {"message": "fastapi server is live!"}

