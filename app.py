import json
import fastapi
import api_model
import dbhandler

from dbhandler import UserControl
from dbhandler import OrbitControl
from dbhandler import SolarControl
from dbhandler import SolarMsgControl
from dbhandler import ChatControl
from dbhandler import SessionControl

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
def logout(session: str):
    result = SessionControl.revoke_session(session)
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

        
# USER LEVEL ACCOUNT MODIFICATION FUNCTIONS

@app.patch('/api/v1/users/modify')
def modify_user(params: str, request: Request):
    sessid = request.cookies.get("session")
    if not sessid:
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





@app.get('/')
def root():
    return {"message": "fastapi server is live!"}

