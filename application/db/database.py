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
            VALUES ({owner_id}, '{link_photo_1}', {likes_count_photo_1}, '{link_photo_2}', {likes_count_photo_2},
            '{link_photo_3}', {likes_count_photo_3})
            """
        connection.execute(insert_query)


def output_search_result(number_of_candidates):
    insert_query = f"""SELECT first_name, last_name, link_photo_1 lp1, link_photo_2 lp2, link_photo_3 lp3
                    FROM sorted_data sd
                    JOIN search_result sr ON sd.owner_id = sr.owner_id
                    WHERE sd.likes_count_photo_3 >= 30
                    LIMIT {number_of_candidates};
                    """
    response = connection.execute(insert_query)
    temp_list = []
    for line in response:
        temp_list.append(line)
    return temp_list
