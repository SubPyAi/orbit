import json

from uuid import UUID
from datetime import date
from pydantic import BaseModel, PrivateAttr, Field, EmailStr, constr, model_validator
from typing import Any, Annotated

class LoginRequest(BaseModel):
    username: str | None = None
    password: str | None = None
    session: UUID | None = None

    @model_validator(mode="after")
    def validate_login_request(self):
        method_uname_pwd = (
            (self.username is not None)
            and (self.password is not None)
        )
        method_session = (self.session is not None)

        if method_session != method_uname_pwd:
            return self
        else:
            raise ValueError("Invalid request")

class LogoutRequest(BaseModel):
    session: UUID | None = None

class GetCurrentUserRequest(BaseModel):
    session: UUID | None = None

class CreateUserRequest(BaseModel):
    username: Annotated[str, constr(min_length=4, max_length=16)]
    password: Annotated[str, constr(min_length=4)]
    email: EmailStr
    phone: Annotated[str, constr(min_length=10, max_length=10)]
    DoB: date
    pfp_ref: UUID | None = None

class GetUserRequest(BaseModel):
    uname: str | None = None
    uid: UUID | None = None

    @model_validator(mode="after")
    def validate_get_user_request(self):
        method_uname = (self.uname is not None)
        method_uid = (self.uid is not None)

        if method_uid != method_uname:
            return self
        else:
            raise ValueError("Invalid request")


class ModifyUserRequest(BaseModel):
    username: str | None = None
    DoB: date | None = None
    pfp_ref: UUID | None = None
    col: str | None = Field(pattern="^#([A-Fa-f0-9]{8})$")
    session: UUID

class SolarConfiguration(BaseModel):
    max_members: int
    allow_edit: bool
    allow_delete: bool
    allow_media: bool
    read_status_visibility: bool
    online_status_visibility: bool

    background_ref: UUID | None = None
    pfp_ref: UUID | None = None

    roles: dict[str, list[str]]
    members: dict[UUID, str]
    ban_list: list[UUID]
    role_map: dict[str, list[UUID]]
    _col_map: dict[UUID, str]

    _json_text: str = PrivateAttr()

    @model_validator(mode="after")
    def validate_configuration(self):
        self._col_map = {}
        for perm_list in self.roles.values():
            for perm in perm_list:
                if perm not in ["send_message", "send_media", "manage_members", "manage_roles", "manage_members", "manage_config", "manage_messages"]:
                    raise ValueError("Invalid Configuration!")
    
        for role_members in self.role_map.values():
            if len(role_members) != len(set(role_members)):
                raise ValueError("Invalid Configuration!")
            if not set(role_members).issubset(set(self.members.keys())):
                raise ValueError("Invalid Configuration!")

        role_mapped_users = set()
        for role, mapped_users in self.role_map.items():
            if role not in self.roles:
                raise ValueError("Invalid Configuration!")
            for user_id in mapped_users:
                if user_id in role_mapped_users:
                    raise ValueError("Invalid Configuration!")
                role_mapped_users.add(user_id)
        if role_mapped_users != set(self.members.keys()):
            raise ValueError("Invalid Configuration!")
        members = {}
        for i in range(len(self.members)):
            members[str(list(self.members.keys())[i])] = list(self.members.values())[i]
        role_map = {}
        for i in self.role_map.keys():
            role_map[i] = []
        for i in range(len(self.role_map.values())):
            for j in range(len(list(self.role_map.values())[i])):
                role_map[str(list(self.role_map.keys())[i])] += [str(list(self.role_map.values())[i][j])]
        for i in self.members.keys():
            self._col_map[i] = "#1b2c3aff"
        self._json_text = json.dumps({
            "max_members": self.max_members,
            "allow_edit": self.allow_edit,
            "allow_delete": self.allow_delete,
            "allow_media": self.allow_media,
            "read_status_visibility": self.read_status_visibility,
            "online_status_visibility": self.online_status_visibility,
            "background_ref": self.background_ref if self.background_ref == None else None,
            "pfp_ref": self.pfp_ref if self.pfp_ref == None else None,
            "roles": self.roles,
            "members": members,
            "ban_list": self.ban_list,
            "role_map": role_map,
            "col_map": self._col_map
        })
        return self

class CreateSolarRequest(BaseModel):
    name: str
    configuration: SolarConfiguration
    session: UUID

class SolarModificationItem(BaseModel):
    id: UUID | None = None
    uname: str | None = None
    role: str | None = None
    perms: list[str] | None = None
    configuration: SolarConfiguration | None = None

class ModifySolarRequest(BaseModel):
    sl_id: UUID
    session: UUID
    key: str
    action: str
    value: list[SolarModificationItem]

class OrbitConfiguration(BaseModel):
    very_close: bool
    background_ref: UUID | None = None
    u_a_col: str = Field(pattern="^#([A-Fa-f0-9]{8})$")
    u_b_col: str = Field(pattern="^#([A-Fa-f0-9]{8})$")

class CreateOrbitRequest(BaseModel):
    user_a: UUID
    user_b: UUID
    configuration: OrbitConfiguration
    session: UUID

class GetOrbitRequest(BaseModel):
    orb_id: UUID
    session: UUID

class ModifyOrbitRequest(BaseModel):
    orb_id: UUID
    session: UUID
    background_ref: UUID | None = None
    col: str = Field(pattern="^#([A-Fa-f0-9]{8})$")

class WSRecv(BaseModel):
    event: str
    data: dict
    id: UUID

class OrbitMessageAttributes(BaseModel):
    col: str = Field(pattern="^#([A-Fa-f0-9]{8})$")
    view_once: bool
    is_media: bool

class OrbitMessage(BaseModel):
    msg_id: UUID
    orb_id: UUID
    id: UUID
    at: date
    edited: int
    attributes: OrbitMessageAttributes

class SolarMessageAttributes(BaseModel):
    col: str = Field(pattern="^#([A-Fa-f0-9]{8})$")
    view_once: bool
    is_media: bool

class SolarMessage(BaseModel):
    msg_id: UUID
    sl_id: UUID
    id: UUID
    at: date
    edited: int
    attributes: OrbitMessageAttributes

class WSProcessUpdation(BaseModel):
    id: UUID
    event: str
    spec_id: UUID | None = "ALL"

class GetSolarRequest(BaseModel):
    id: UUID
    sl_id: UUID
