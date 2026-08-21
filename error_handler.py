class ErrorCodes:
    def __init__(self):
        self.DB_ERROR = 67
        self.USER_ALREADY_EXISTS = 101
        self.USER_NOT_FOUND = 102
        self.USER_NOT_VALIDATED = 103
        self.VERIFICATION_TOKEN_DUPLICACY = 104
        self.SMTP_ERROR = 105
        self.NO_ACTIVE_VERIFICATION_REQUEST = 106
        self.INVALID_VERIFICATION_TOKEN = 107
        self.NON_EXISTENT_SOLAR = 108
        self.ROLE_ALREADY_EXISTS = 109
        self.ROLE_IS_NOT_EMPTY = 110
        self.USER_NOT_SOLAR_MEMBER = 111
        self.USER_BANNED = 112
        self.SOLAR_FULL = 113
        self.USER_NOT_BANNED = 114
        self.INVALID_INPUT_FORMAT = 115
        self.NO_USER_LOGGED_IN = 116
        self.UNAUTHORISED_REQUEST = 117
        self.INSUFFICIENT_PERMISSION = 118
        self.ROLE_DOES_NOT_EXIST = 119
        self.ORBIT_ALREADY_EXISTS = 120
        self.SESSION_EXPIRED = 121
        self.BAD_WS_REQ = 122
        self.ORBIT_DOES_NOT_EXIST = 123
        self.DELETION_NOT_ALLOWED_IN_SOLAR = 124
        self.MESSAGE_DOES_NOT_EXIST = 125
        self.EDITING_NOT_ALLOWED_IN_SOLAR = 126
        self.MEDIA_NOT_ALLOWED_IN_SOLAR = 127


class OrbitException(Exception):
    def __init__(self, error_code: int, cust_text: str = None, ws: bool = False):
        super().__init__(cust_text)
        self.error_code = error_code
        self.cust_text = cust_text
        self.ws = ws

    def response_body(self):
        messages = {
            error_codes.DB_ERROR: "Internal database error",
            error_codes.USER_ALREADY_EXISTS: "User already exists",
            error_codes.USER_NOT_FOUND: "User not found",
            error_codes.USER_NOT_VALIDATED: "User credentials are not valid",
            error_codes.VERIFICATION_TOKEN_DUPLICACY: "Verification token already exists",
            error_codes.SMTP_ERROR: "Unable to send verification email",
            error_codes.NO_ACTIVE_VERIFICATION_REQUEST: "No active verification request",
            error_codes.INVALID_VERIFICATION_TOKEN: "Invalid verification token",
            error_codes.NON_EXISTENT_SOLAR: "Solar not found",
            error_codes.ROLE_ALREADY_EXISTS: "Role already exists or was not found",
            error_codes.ROLE_IS_NOT_EMPTY: "Role is not empty",
            error_codes.USER_NOT_SOLAR_MEMBER: "User is not a solar member",
            error_codes.USER_BANNED: "User is banned",
            error_codes.SOLAR_FULL: "Solar is full",
            error_codes.USER_NOT_BANNED: "User is not banned",
            error_codes.INVALID_INPUT_FORMAT: "Invalid request format",
            error_codes.NO_USER_LOGGED_IN: "No logged in user",
            error_codes.UNAUTHORISED_REQUEST: "Unauthorised request",
            error_codes.INSUFFICIENT_PERMISSION: "Current permissions are insufficient for the modification",
            error_codes.ROLE_DOES_NOT_EXIST: "The requested role does not exist",
            error_codes.ORBIT_ALREADY_EXISTS: "The requested orbit alreasy exists",
            error_codes.SESSION_EXPIRED: "The current session has been expired",
            error_codes.BAD_WS_REQ: "Bad WebSocket Request",
            error_codes.ORBIT_DOES_NOT_EXIST: "Orbit does not exist",
            error_codes.DELETION_NOT_ALLOWED_IN_SOLAR: "Message deletion is not allowed in this solar",
            error_codes.MESSAGE_DOES_NOT_EXIST: "Message does not exist",
            error_codes.EDITING_NOT_ALLOWED_IN_SOLAR: "Message editing is not allowed in this solar",
            error_codes.MEDIA_NOT_ALLOWED_IN_SOLAR: "Media communication is not allowed in this solar"
        }
        return {
            "status": self.error_code,
            "body": self.cust_text or messages.get(self.error_code, "Unknown error"),
        }


error_codes = ErrorCodes()