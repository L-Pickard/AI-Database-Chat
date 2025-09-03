from schedule import every, run_pending
from time import sleep
from Create_db import create_datbase
import os
import sys

def restart_program():
    try:
        os.execv(sys.executable, ['python'] + [os.path.join(sys.path[0], 'Chat.py')] + sys.argv[1:])
    except Exception as e:
        os.system(f'python "{os.path.join(sys.path[0], "Chat.py")}"')

if __name__ == "__main__":

    restart_program()

    every().day.at("17:00").do(create_datbase)

    while True:
        run_pending()
        sleep(1)