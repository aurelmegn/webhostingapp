from src import app
from src.utils.find_or_create import find_or_create

if __name__ == "__main__":
    # make sure the some directories exists

    from os.path import join

    try:

        find_or_create(app.config.get("FTP_BASE_DIR"))
        find_or_create(join(app.config.get("SUPERVISOR_CONFIG_DIR"), "programs"))

        app.run(host="0.0.0.0", port=5000)

    except Exception as e:
        print(e)
        exit(1)
