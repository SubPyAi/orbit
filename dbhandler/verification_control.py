import hashlib
import dotenv
import hmac
import smtplib
from email.message import EmailMessage
import uuid
from error_handler import ErrorCodes
from dbhandler import sql_handler

dotenv.load_dotenv('.env')

SMTP_SERVER = dotenv.get_key('.env', "BREVO_SMTP_SERVER_HOST")
SMTP_PORT = dotenv.get_key('.env', "BREVO_SMTP_SERVER_PORT")
SMTP_LOGIN = dotenv.get_key('.env', "BREVO_SMTP_LOGIN")
SMTP_KEY = dotenv.get_key('.env', "BREVO_SMTP_KEY")
error_codes = ErrorCodes()

class VerificationControl:

    def add_new_verification(id, user_identifier, token, type):
        token = token.upper()
        v_id = str(uuid.uuid4())
        if type == 'email':
            token_hash = hashlib.sha256(token.encode('utf-8')).hexdigest()
            req_existing_token = sql_handler.put_query("select * from VerificationBlock where token_hash = %s;", (token_hash, ))
            if req_existing_token != []:
                return error_codes.VERIFICATION_TOKEN_DUPLICACY
            else:
                msg = EmailMessage()
                msg["Subject"] = "Email verification mail from Orbit"
                msg["From"] = "noreply.orbitservers@gmail.com"
                msg["To"] = user_identifier
                verification_code = token
                msg.set_content("Here is your Orbit verification code: \n\n\n\n \t\t%s \n\n\n\nThank you for using Orbit!" % verification_code)

                try:
                    with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
                        server.starttls()
                        server.login(SMTP_LOGIN, SMTP_KEY)
                        server.send_message(msg)
                except Exception as e:
                    print("[SMTP] Error:", type(e).__name__, str(e))
                    return error_codes.SMTP_ERROR

                sql_handler.put_query("update VerificationBlock set used = 1 where id = '" + id + "' and identifier = 'email';")
                sql_handler.put_query("insert into VerificationBlock (v_id, id, identifier, token_hash) values (%s, %s, 'email', %s)", (v_id, id, token_hash))
                return 0

    def validate_token(id, token):
        query = "select * from VerificationBlock where id = %s and used = 0"
        params = (id,)
        res = sql_handler.put_query(query, params)
        if res == error_codes.DB_ERROR:
            return error_codes.DB_ERROR
        elif res == []:
            return error_codes.NO_ACTIVE_VERIFICATION_REQUEST
        else:
            verified = hmac.compare_digest(hashlib.sha256(token.encode('utf-8')).hexdigest(), res[0][3])
            if verified:
                sql_handler.put_query("update VerificationBlock set used = 1 where v_id = %s;", (res[0][0],))
                return 0
            else:
                return error_codes.INVALID_VERIFICATION_TOKEN