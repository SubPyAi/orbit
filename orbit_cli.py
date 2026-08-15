import subprocess

print("Orbit CLI is supposed to be a strictly server-side backend testing application. It is not intended for end-users.")
print("This application will just start a python shell with all the backend functions imported and ready to use. You can use this shell to test the backend functions of Orbit.")

subprocess.call(['python', '-i', '-c', 'import dbhandler; import orbvarhandler; from dbhandler.chat_control import ChatControl; from dbhandler.orbit_control import OrbitControl; from dbhandler.session_control import SessionControl; from dbhandler.solar_control import SolarControl; from dbhandler.solar_msg_control import SolarMsgControl; from dbhandler.user_control import UserControl; from orbvarhandler.var_calculator import VarCalculator;'])