import subprocess

print("Orbit CLI is supposed to be a strictly server-side backend testing application. It is not intended for end-users.")
print("This application will just start a python shell with all the backend functions imported and ready to use. You can use this shell to test the backend functions of Orbit.")

subprocess.call(['python', '-i', '-c', 'import dbhandler;'])