from os import kill, remove
from os.path import isfile
from signal import SIGHUP
from time import sleep

from src import app


def main():

    with open(app.config.get("NGINX_PID_FILE")) as pid_content:
        nginx_pid = int(pid_content.readline())

    nginx_file_check_hup_signal_from_path = app.config.get("NGINX_HUP_CHECK_FILE")

    while True:
        sleep(60)
        print("Sleeping...")
        if isfile(nginx_file_check_hup_signal_from_path):
            print("Sending SIGHUP to nginx ||")
            remove(nginx_file_check_hup_signal_from_path)
            kill(nginx_pid, SIGHUP)


if __name__ == "__main__":
    main()
