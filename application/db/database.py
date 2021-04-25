import sqlalchemy
from application.db.user_information import DB


engine = sqlalchemy.create_engine(f"postgresql://{DB['db_owner']}:{DB['password']}@localhost:5432/{DB['db_name']}")

connection = engine.connect()
user_id = []


def get_user_info(owner_id: int, user_name: str):
    """
    :param owner_id: int
    :param user_name: str
    :return: str
    """
    user_id.append(owner_id)
    insert_query = f"""INSERT INTO main_user (user_id, first_name, last_name)
        VALUES ({owner_id}, '{user_name.split()[0]}', '{user_name.split()[1]}')
        """
    connection.execute(insert_query)


def get_people_information(data: list):
    """
    :param data: list
    :return: str
    """
    owner_id = data[-1]
    first_name = data[0].split()[0]
    last_name = data[0].split()[-1]
    insert_query = f"""INSERT INTO search_result
        (user_id, owner_id, first_name, last_name)
        VALUES ({user_id[-1]}, {owner_id}, '{first_name}', '{last_name}')
        """
    connection.execute(insert_query)


def get_most_of_liked_photos(owner_id: int, data: list):
    """
    :param owner_id: int
    :param data: list
    """
    if len(data) != 3:
        pass
    else:
        link_photo_1, likes_count_photo_1 = data[0][0], data[0][1]
        link_photo_2, likes_count_photo_2 = data[1][0], data[1][1]
        link_photo_3, likes_count_photo_3 = data[2][0], data[2][1]

        insert_query = f"""INSERT INTO sorted_data (owner_id, link_photo_1,
            likes_count_photo_1, link_photo_2, likes_count_photo_2, link_photo_3, likes_count_photo_3)
            VALUES ({owner_id},'{link_photo_1}', {likes_count_photo_1}, '{link_photo_2}', {likes_count_photo_2},
            '{link_photo_3}', {likes_count_photo_3})
            """
        connection.execute(insert_query)


def get_owner_id_list():
    id_list = []
    result = connection.execute("SELECT owner_id FROM viewed_candidates")
    for owner_id in result:
        owner_id = str(owner_id)
        owner_id = owner_id.strip('(,)')
        id_list.append(owner_id)
    return id_list


def output_search_result(number_of_candidates):
    insert_query = f"""SELECT sd.owner_id, first_name, last_name, link_photo_1, link_photo_2, link_photo_3
                    FROM sorted_data sd
                    JOIN search_result sr ON sd.owner_id = sr.owner_id
                    LIMIT {number_of_candidates};
                    """
    response = connection.execute(insert_query)
    temp_list = []
    for line in response:
        name = f'{line[1]} {line[2]}'
        add_owner_id = f"""INSERT INTO viewed_candidates (owner_id, name) VALUES ({int(line[0])}, '{name}')"""
        connection.execute(add_owner_id)
        joined_line = f'ID:{int(line[0])} | {name} Photo_1: {line[3]} Photo_2: {line[4]} Photo_3: {line[-1]}'
        temp_list.append(int(line[0]))
        temp_list.append(joined_line)
    return temp_list


def add_favorite(owner_id: int, data: list):
    connection.execute(f"""INSERT INTO favorites (owner_id, photo_link)
                        VALUES ({owner_id}, '{data}')""")
    return 'favorite added'


def add_to_ban_list(owner_id: int):
    connection.execute(f"""INSERT INTO ban_list (owner_id)
                            VALUES ({owner_id})""")
    return 'add to ban list'


def clear_database():
    connection.execute("""TRUNCATE sorted_data; TRUNCATE search_result; TRUNCATE main_user;""")
    return 'EMPTY DATABASE'
