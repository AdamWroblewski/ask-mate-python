import csv
import os
import psycopg2
import psycopg2.extras


QUESTION_HEADERS = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']
ANSWER_HEADERS = ['id', 'submission_time', 'vote_number', 'question_id', 'message', 'image']


def read_csv_data(file_name):
    post_list = []
    with open(file_name) as posts:
        reader = csv.DictReader(posts)

        for post in reader:
            post_list.append(post)

    return post_list


def append_csv_data(file_name, data, fieldnames):
    with open(file_name, 'a') as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)

        writer.writerow(data)


def create_connection_string():
    user_name = os.environ.get('PSQL_NAME')
    host = os.environ.get('PSQL_HOST')
    data_base = os.environ.get('PSQL_DB')
    password = os.environ.get('PSQL_PASS')

    connection_string_defined = user_name and host and data_base and password

    if connection_string_defined:
        return f'postgres://{user_name}:{password}@{host}/{data_base}'
    else:
        raise KeyError('Some necessary environment variable(s) are not defined')


def open_database():
    try:
        connection_string = create_connection_string()
        connection = psycopg2.connect(connection_string)
        connection.autocommit = True
    except psycopg2.DatabaseError as exception:
        print('Database connection problem')
        raise exception
    return connection


def connection_handler(function):
    def wrapper(*args, **kwargs):
        connection = open_database()
        # we set the cursor_factory parameter to return with a RealDictCursor cursor (cursor which provide dictionaries)
        dict_cur = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        ret_value = function(dict_cur, *args, **kwargs)
        dict_cur.close()
        connection.close()
        return ret_value

    return wrapper
