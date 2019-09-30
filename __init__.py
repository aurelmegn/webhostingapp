from src import app


def find_or_create(directory: str):
    from os import mkdir
    from os.path import exists, abspath

    abs_path = abspath(directory)

    if not exists(abs_path):
        mkdir(abs_path)


if __name__ == "__main__":
    # make sure the some directories exists

    from os.path import join

    try:

        find_or_create(app.config.get("FTP_BASE_DIR"))
        find_or_create(join(app.config.get("SUPERVISOR_CONFIG_DIR"), "programs"))

        app.run(host="0.0.0.0", port=8000)

    except Exception as e:
        print(e)
        exit(1)
