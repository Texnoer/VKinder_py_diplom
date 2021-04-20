import sqlalchemy
from application.db.user_information import DB


engine = sqlalchemy.create_engine(f"postgresql://{DB['db_owner']}:{DB['password']}@localhost:5432/{DB['db_name']}")

connection = engine.connect()


def get_user_info(user_id: int, user_name: str):
    """
    :param user_id: int
    :param user_name: str
    :return: str
    """

    insert_query = f"""INSERT INTO main_user (user_id, first_name, last_name)
        VALUES ({user_id}, '{user_name.split()[0]}', '{user_name.split()[1]}')
        """
    connection.execute(insert_query)


def get_people_information(data: dict):
    """
    :param data: dict
    :return: str
    """
    for value in data.values():
        owner_id = value[-1]
        first_name = value[0]
        last_name = value[1]
        insert_query = f"""INSERT INTO search_result
            (owner_id, first_name, last_name)
            VALUES ({owner_id}, '{first_name}', '{last_name}')
            """
        connection.execute(insert_query)


def get_most_liked_photos():
    pass
