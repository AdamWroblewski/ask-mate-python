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
                            WHERE id = %(question_id)s;
                           """, {'question_id': question_id})
    question_dict = cursor.fetchall()

    return question_dict


@connection.connection_handler
def get_all_sorted_answers(cursor, question_id):

    cursor.execute(sql.SQL("""
                            SELECT * FROM answer
                            WHERE question_id = {question_id}
                            ORDER BY submission_time;
                           """).format(question_id=sql.Literal(question_id)))

    answers_dict = cursor.fetchall()

    return answers_dict


@connection.connection_handler
def find_max_id(cursor):

    cursor.execute("SELECT max(id) FROM question;")

    DICT_INDEX_WITH_PARAMETER = 0
    newest_id_question = cursor.fetchall()

    return newest_id_question[DICT_INDEX_WITH_PARAMETER]['max']


@connection.connection_handler
def get_column_headers(cursor, table_header):

    cursor.execute("""
                    SELECT column_name
                    FROM INFORMATION_SCHEMA.COLUMNS
                    WHERE TABLE_NAME = {table_header};
                   """).format(table_header=sql.Literal(table_header))

    table_header_dict = cursor.fetchall()

    return table_header_dict


@connection.connection_handler
def add_new_question(cursor, title, message, img=None):

    sql_query = """INSERT INTO 
                    question (submission_time, view_number, vote_number, title, message, image)
                    VALUES (now(), 0, 0, %s, %s, %s);"""

    cursor.execute(sql_query, (title, message, img))


@connection.connection_handler
def add_new_answer(cursor, message, question_id, img=None):

    sql_query = """
                INSERT INTO
                answer (submission_time, vote_number, question_id, message, image)
                VALUES (date_trunc('second', now()), 0, %s, %s, %s);
                """

    cursor.execute(sql_query, (question_id, message, img))


@connection.connection_handler
def get_question_ids(cursor):

    cursor.execute('SELECT id FROM question;')

    question_ids = cursor.fetchall()
    ids_list = []

    for dict in question_ids:
        ids_list.append(dict['id'])

    return ids_list


@connection.connection_handler
def insert_question_comment(cursor, question_id, message):

    sql_query = """
                INSERT INTO
                comment (question_id, message, submission_time, edited_count)
                VALUES (%s, %s, date_trunc('second', now()), 0);
                """

    cursor.execute(sql_query, (question_id, message))


@connection.connection_handler
def get_question_comments(cursor, question_id):

    cursor.execute("""
                    SELECT message, submission_time FROM comment
                    WHERE question_id = %(question_id)s;
                   """, {'question_id': question_id})

    question_comment_dict = cursor.fetchall()
    return question_comment_dict


@connection.connection_handler
def insert_answer_comment(cursor, answer_id, message):

    sql_query = """
                INSERT INTO
                comment (answer_id, message, submission_time, edited_count)
                VALUES (%s, %s, date_trunc('second', now()), 0);
                """

    cursor.execute(sql_query, (answer_id, message))


@connection.connection_handler
def get_answer_coments(cursor, *args):

    sql_query = """
                select answer_id, c.message, c.submission_time from answer as a
                right join "comment" as c
                on a.id = c.question_id
                where c.answer_id in %s;
                """

    cursor.execute(sql_query, args)
    answer_comments_dict = cursor.fetchall()

    return answer_comments_dict


def get_answers_ids(question_id):
    answers_dict = get_all_sorted_answers(question_id)

    id_list = list()
    for answer in answers_dict:
        id_list.append(answer['id'])

    return tuple(id_list)


@connection.connection_handler
def search_phrase_in_answer(cursor, phrase):

    sql_query = """SELECT * FROM question as q
                   JOIN answer as a ON a.question_id=q.id
                   WHERE q.message LIKE %(phrase)s
                   OR a.message LIKE %(phrase)s"""

    cursor.execute(sql_query, {'phrase': f'%{phrase}%'})

    result = cursor.fetchall()
    return result


@connection.connection_handler
def search_phrase_in_question(cursor, phrase):

    sql_query = """SELECT * FROM question
                   WHERE title LIKE %(phrase)s
                   OR message LIKE %(phrase)s"""

    cursor.execute(sql_query, {'phrase': f'%{phrase}%'})

    result = cursor.fetchall()
    return result


@connection.connection_handler
def save_user_data(cursor, login, password):

    sql_query = """
                INSERT INTO ask_mate_users
                VALUES (default, default, %(login)s, %(password)s, 'mail', 0)
                """

    cursor.execute(sql_query, {'login': login, 'password': password})
