from psycopg2 import sql

import connection


@connection.connection_handler
def get_all_questions(cursor):

    cursor.execute("""
                    SELECT * FROM question
                    ORDER BY submission_time;
                   """)

    title_dict = cursor.fetchall()
    return title_dict


@connection.connection_handler
def get_question_by_id(cursor, question_id):

    cursor.execute("""
                            SELECT * FROM question
                            WHERE id = %(question_id)s
                           """, {'question_id': question_id})
    question_dict = cursor.fetchall()

    return question_dict


@connection.connection_handler
def get_all_sorted_answers(cursor, question_id):

    cursor.execute(sql.SQL("""
                            SELECT * FROM answer
                            WHERE question_id = question_id
                            ORDER BY submission_time
                           """).format(question_id=sql.Literal(question_id)))

    answers_dict = cursor.fetchall()

    return answers_dict


@connection.connection_handler
def find_max_id(cursor):

    cursor.execute("""
                SELECT max(id) FROM question
                """)

    DICT_INDEX_WITH_PARAMETER = 0
    newest_id_question = cursor.fetchall()

    return newest_id_question[DICT_INDEX_WITH_PARAMETER]['max']

@connection.connection_handler
def get_column_headers(cursor, table_header):

    cursor.execute("""
                    SELECT column_name
                    FROM INFORMATION_SCHEMA.COLUMNS
                    WHERE TABLE_NAME = table_header 
                   """).format(table_header=sql.Literal(table_header))

    table_header_dict = cursor.fetchall()

    return table_header_dict


@connection.connection_handler
def add_new_question(cursor, title, message, img=None):

    sql_query = """INSERT INTO 
                    question (submission_time, view_number, vote_number, title, message, image)
                    VALUES (now(), 0, 0, %s, %s, %s)"""

    cursor.execute(sql_query, (title, message, img))


@connection.connection_handler
def add_new_answer(cursor, message, question_id, img=None):

    sql_query = """
                INSERT INTO
                answer (submission_time, vote_number, question_id, message, image)
                VALUES (now(), 0, %s, %s, %s)
                """

    cursor.execute(sql_query, (question_id, message, img))


@connection.connection_handler
def get_question_ids(cursor):

    cursor.execute("""
                SELECT id FROM question
                """)

    question_ids = cursor.fetchall()
    ids_list = []
    
    for dict in question_ids:
        ids_list.append(dict['id'])

    return ids_list
