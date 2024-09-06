import os.path
from typing import List
from src.util.connection_pool import Connection


def init_db(files: List[str], connection: Connection) -> None:
    connection.autocommit = False
    try:
        for file in files:
            relative_path_file = os.path.join(os.getcwd(), 'sql', file)
            print(relative_path_file)
            if not os.path.isfile(relative_path_file):
                raise FileNotFoundError(f'File with path: "{relative_path_file}" not found')
            with open(relative_path_file, encoding='utf-8') as f:
                data = f.read()
                connection.executescript(data)
        connection.commit()
    except Exception as e:
        raise e
    finally:
        if connection:
            connection.rollback()
            connection.autocommit = True
            connection.close()
