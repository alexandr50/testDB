import pathlib

from utils.config import config
from classes.database import DBManager

dir_path = pathlib.Path.cwd()
PATH_TO_DB_CONFIG = pathlib.Path(dir_path, 'database.ini')


def main():
    params = config(PATH_TO_DB_CONFIG)
    db = DBManager('shop', params)
    db.create_database()

if __name__ == '__main__':
    main()
