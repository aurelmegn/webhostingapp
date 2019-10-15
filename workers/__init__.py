import sys

from os import makedirs
from os.path import isdir, join

from src import app
# sys.path.append(".")
# sys.path.append("../")
import logging
from workers.app_state_updater import run_threads


# log file
log_dir = "./src/var/log"
if not isdir(log_dir):
    makedirs(log_dir)

if bool(app.config.get("DEBUG")):
    log_file = "dev.log"
else:
    log_file = "prod.log"
log_file = join(log_dir, log_file)

app_file_log_handler = logging.FileHandler(log_file)
app_file_log_handler.setLevel(logging.DEBUG)

run_threads()
app.logger.info("lll")
