import json
import fastapi
import secrets
import api_model
import error_handler
import dbhandler

from error_handler import ErrorCodes
from error_handler import OrbitException

from api_model import LoginRequest
from api_model import LogoutRequest
from api_model import GetCurrentUserRequest
from api_model import CreateUserRequest
from api_model import GetUserRequest
from api_model import ModifyUserRequest
from api_model import CreateSolarRequest
from api_model import ModifySolarRequest
from api_model import SolarConfiguration

from dbhandler import UserControl
from dbhandler import OrbitControl
from dbhandler import SolarControl
from dbhandler import SolarMsgControl
from dbhandler import ChatControl
from dbhandler import SessionControl
from dbhandler import VerificationControl

from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError

# FASTAPI INITIALISATION
app = fastapi.FastAPI()
error_codes = ErrorCodes()

# ORBIT ERROR HANDLERS

@app.exception_handler(RequestValidationError)
async def validation_error_handler(
    request: Request,
    exc: RequestValidationError
):
    return JSONResponse(
        status_code=200,
        content={
            "status": error_codes.INVALID_INPUT_FORMAT,
            "error": "invalid_input_format"
        }
    )

@app.exception_handler(OrbitException)
async def exception(request: Request, orbit_exception: OrbitException):
    return JSONResponse(status_code=200, content=orbit_exception.response_body())


def raise_for_error(result):
    if isinstance(result, bool):
        return result
    if isinstance(result, int) and result in vars(error_codes).values():
        raise OrbitException(result)
    return result

#
# Orbit API v1
#

# LOGIN AUTHENTICATION FUNCTIONS

@app.post('/api/v1/auth/login')
def login(params: LoginRequest):
    username = params.username
    password = params.password
    session = str(params.session)
    if username and password:
        result1 = UserControl.validate_user(username, password)
        raise_for_error(result1)
        if result1 == 0:
            result2 = SessionControl.create_session(UserControl.get_uid(username))
            raise_for_error(result2)
            response = JSONResponse({"status": 0, "auth_status": 0})
            response.set_cookie(
                key = "session",
                value = result2,
                httponly = True,
                secure = True,
                samesite = "lax", 
                path = "/"
            )
            return response
    else:
        result = SessionControl.validate_session(session)
        raise_for_error(result)
        if result:
            return {"status": 0, "auth_status": 0}
        else:
            return {"status": 0, "auth_status": 1}

@app.post('/api/v1/auth/logout')
def logout(params: Request):
    sessionid = str(params.cookies.get('session'))
    result = SessionControl.revoke_session(sessionid)
    raise_for_error(result)
    response = JSONResponse({"auth_status": 1})
    response.delete_cookie(key = "session")
    return response

@app.get('/api/v1/auth/me')
def get_current_user(params: Request):
    sess_id = str(params.cookies.get('session'))
    if sess_id:
        req = SessionControl.validate_session(sess_id)
        raise_for_error(req)
        if req:
            session = SessionControl.get_session(sess_id)
            raise_for_error(session)
            return {"status": 0, "uid": session.id}
        else:
            return {"status": 0, "uid": None}
    else:
        raise_for_error(error_codes.NO_USER_LOGGED_IN)


# SIGN UP AUTHENTICATION FUNCTIONS

@app.post('/api/v1/signup/create')
def create_new_user(params: CreateUserRequest):
    username = params.username
    password = params.password
    email = params.email
    phone = params.phone
    DoB = str(params.DoB)
    pfp_ref = params.pfp_ref
    result = UserControl.create_user(username, password, email, phone, DoB, pfp_ref)
    raise_for_error(result)
    return {"status": 0, "account_creation": "success"}

# GENERAL LEVEL USER QUERY FUNCTIONS

@app.get('/api/v1/users/get')
def get_user(params: GetUserRequest):
    uname = params.uname
    uid = params.uid
    if uname:
        user =  UserControl.get_user(UserControl.get_uid(uname))
        raise_for_error(user)
        return {"status": 0, "username": user.username, "DoB": user.DoB, "created": user.created, "pfp_ref": user.pfp_ref}
    else:
        user =  UserControl.get_user(uid)
        raise_for_error(user)
        return {"status": 0, "username": user.username, "DoB": user.DoB, "created": user.created, "pfp_ref": user.pfp_ref}


# USER VERIFICATION FUNCTIONS

def send_new_verification_email(id, email):
    return VerificationControl.add_new_verification(id, email, "".join([str(secrets.randbelow(10)) for _ in range(6)]), 'email')

def verify_token(id, token):
    return VerificationControl.validate_token(id, token)
        
# USER LEVEL ACCOUNT MODIFICATION FUNCTIONS

@app.patch('/api/v1/users/modify')
def modify_user(params: ModifyUserRequest):
    sessid = str(params.session)
    if sessid:
        result = SessionControl.validate_session(sessid)
        raise_for_error(result)
        if result:
            session = SessionControl.get_session(sessid)
            raise_for_error(session)
            user = UserControl.get_user(session.id)
            raise_for_error(user)
            res = UserControl.update_user(user.id, params.username if params.username else None, None, None, None, str(params.DoB) if params.DoB else None, str(params.pfp_ref) if params.pfp_ref else None)
            raise_for_error(res)
            return {"status": 0}
        else:
            response = JSONResponse({"status": 0, "auth_status": 1})
            response.delete_cookie('session')
            return response
    else:
        raise_for_error(error_codes.UNAUTHORISED_REQUEST)

# SOLAR CRUD

@app.post('/api/v1/solars/create')
def create_solar(params: CreateSolarRequest):
    session = SessionControl.get_session(str(params.session))
    raise_for_error(session)
    res = SolarControl.create_solar(session.id, params.name, params.configuration._json_text)
    raise_for_error(res)
    return {"status": 0, "sl_id": res}

@app.get('/api/v1/solars/get/{sl_id}')
def get_solar(sl_id: str):
    solar = SolarControl.get_solar(sl_id)
    raise_for_error(solar)
    return {"status": 0, "sl_id": solar.sl_id, "id": solar.id, "name": solar.name, "configuration": solar.configuration, "created": solar.created}

@app.get('/api/v1/solars/mysolars')
def get_user_solars(request: Request):
    session = SessionControl.get_session(request.cookies.get('session'))
    raise_for_error(session)
    solars = SolarControl.get_solars(session.id)
    raise_for_error(solars)
    return {"status": 0, "solars": solars}

@app.post('/api/v1/solars/{sl_id}/leave')
def leave_solar(sl_id: str, request: Request):
    session = SessionControl.get_session(request.cookies.get('session'))
    raise_for_error(session)
    

    result = SolarControl.remove_member(sl_id, session.id)
    raise_for_error(result)
    return {"status": 0}

@app.patch('/api/v1/solars/modify')
def modify_solar(params: ModifySolarRequest):
    sl_id = str(params.sl_id)
    key = params.key
    action = params.action
    session = SessionControl.get_session(str(params.session))
    raise_for_error(session)
    perms = SolarControl.get_user_permissions(sl_id, session.id)
    value = params.value
    if key == 'members':
        if "manage_members" in perms:
            if action == 'add':
                for i in value:
                    if not (i.id and i.uname and i.role):
                        raise_for_error(error_codes.INVALID_INPUT_FORMAT)
                    res = SolarControl.add_member(sl_id, str(i.id), i.uname, i.role)
                    raise_for_error(res)
                return {"status": 0}
            elif action == 'remove':
                for i in value:
                    if not i.id:
                        raise_for_error(error_codes.INVALID_INPUT_FORMAT)
                    res = SolarControl.remove_member(sl_id, str(i.id))
                    raise_for_error(res)
                return {"status": 0}
            elif action == 'ban':
                for i in value:
                    if not i.id:
                        raise_for_error(error_codes.INVALID_INPUT_FORMAT)
                    res = SolarControl.remove_member(sl_id, str(i.id))
                    raise_for_error(res)
                    ban_result = SolarControl.ban_member(sl_id, str(i.id))
                    raise_for_error(ban_result)
                return {"status": 0}
            elif action == 'unban':
                for i in value:
                    if not i.id:
                        raise_for_error(error_codes.INVALID_INPUT_FORMAT)
                    res = SolarControl.unban_member(sl_id, str(i.id))
                    raise_for_error(res)
                return {"status": 0}
            else:
                raise_for_error(error_codes.INVALID_INPUT_FORMAT)
        else:
            raise_for_error(error_codes.INSUFFICIENT_PERMISSION)
    elif key == 'roles':
        if "manage_roles" in perms:
            if action == 'add':
                for i in value:
                    if not (i.role and i.perms):
                        raise_for_error(error_codes.INVALID_INPUT_FORMAT)
                    res = SolarControl.add_role(sl_id, i.role, i.perms)
                    raise_for_error(res)
                return {"status": 0}
            elif action == 'remove':
                for i in value:
                    if not i.role:
                        raise_for_error(error_codes.INVALID_INPUT_FORMAT)
                    res = SolarControl.remove_role(sl_id, i.role)
                    raise_for_error(res)
                return {"status": 0}
            elif action == 'assign':
                for i in value:
                    if not (i.id and i.role):
                        raise_for_error(error_codes.INVALID_INPUT_FORMAT)
                    res = SolarControl.assign_role(sl_id, str(i.id), i.role)
                    raise_for_error(res)
                return {"status": 0}
            else:
                raise_for_error(error_codes.INVALID_INPUT_FORMAT)
        else:
            raise_for_error(error_codes.INSUFFICIENT_PERMISSION)
    elif key == 'config':
        if "manage_config" not in perms:
            raise_for_error(error_codes.INSUFFICIENT_PERMISSION)

        if not value[0].configuration:
            raise_for_error(error_codes.INVALID_INPUT_FORMAT)

        if action != 'set':
            raise_for_error(error_codes.INVALID_INPUT_FORMAT)

        if not isinstance(value, dict):
            raise_for_error(error_codes.INVALID_INPUT_FORMAT)

        res = SolarControl.update_solar(sl_id, value[0]['configuration'].json_text)
        raise_for_error(res)
        return {"status": 0}
    else:
        raise_for_error(error_codes.INVALID_INPUT_FORMAT)
                    
@app.get('/')
def root():
    return {"message": "fastapi server is live!"}

