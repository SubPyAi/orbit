import os
import subprocess
import keyboard

print("Orbit CLI is supposed to be a strictly server-side backend testing application. It is not intended for end-users.")
print("\n\nThis application will just start a python shell with all the backend functions imported and ready to use. You can use this shell to test the backend functions of Orbit.")
print("\n\n\n")

print("[Orbit CLI] Current working directory: " + os.getcwd() + "\n\n")
subprocess.call(['python', '-i', '-c', 'import keyboard; import dbhandler; import orbvarhandler; from dbhandler.chat_control import ChatControl; from dbhandler.orbit_control import OrbitControl; from dbhandler.session_control import SessionControl; from dbhandler.solar_control import SolarControl; from dbhandler.solar_msg_control import SolarMsgControl; from dbhandler.user_control import UserControl; from dbhandler.verification_control import VerificationControl; from orbvarhandler.var_calculator import OrbitVarCalculator; from orbvarhandler.var_calculator import SolarVarCalculator; keyboard.press("return");'])

print("\n\n\n\n\n\n\n\n[Orbit CLI] Process Terminated, press q to exit")

while not keyboard.is_pressed('q'):
    pass