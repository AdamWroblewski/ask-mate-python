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

    cursor.execute("""
                            SELECT * FROM answer
                            WHERE question_id = %(question_id)s
                            ORDER BY submission_time;
                           """, {'question_id': question_id})

    answers_dict = cursor.fetchall()

    return answers_dict


@connection.connection_handler
def find_max_id(cursor):

    cursor.execute("SELECT max(id) FROM question;")

    newest_id_question = cursor.fetchall()
    return newest_id_question[0]['max']


@connection.connection_handler
def add_new_question(cursor, title, message, user_id, img=None):

    sql_query = """INSERT INTO 
                    question (submission_time, view_number, vote_number, title, message, image, user_id)
                    VALUES (now(), 0, 0, %s, %s, %s, %s);"""

    cursor.execute(sql_query, (title, message, img, user_id))


@connection.connection_handler
def add_new_answer(cursor, message, question_id, user_id, img=None):

    sql_query = """
                INSERT INTO
                answer (submission_time, vote_number, question_id, message, user_id, image)
                VALUES (date_trunc('second', now()), 0, %s, %s, %s, %s);
                """

    cursor.execute(sql_query, (question_id, message, user_id, img))


@connection.connection_handler
def get_question_ids(cursor):

    cursor.execute('SELECT id FROM question;')

    question_ids = cursor.fetchall()
    ids_list = []

    for dict in question_ids:
        ids_list.append(dict['id'])

    return ids_list

@connection.connection_handler
def get_question_by_answer_id(cursor, answer_id):
    cursor.execute("SELECT question_id FROM answer WHERE id = %(answer_id)s", {'answer_id': answer_id})
    question_id = cursor.fetchone()
    return question_id # {'question_id': 1} or None;
#

@connection.connection_handler
def insert_question_comment(cursor, question_id, message, user_id):

    sql_query = """
                INSERT INTO
                comment (question_id, message, submission_time, edited_count, user_id)
                VALUES (%s, %s, date_trunc('second', now()), 0, %s);
                """

    cursor.execute(sql_query, (question_id, message, user_id))


@connection.connection_handler
def get_question_comments(cursor, question_id):

    cursor.execute("""
                    SELECT message, submission_time FROM comment
                    WHERE question_id = %(question_id)s;
                   """, {'question_id': question_id})

    question_comment_dict = cursor.fetchall()
    return question_comment_dict


@connection.connection_handler
def insert_answer_comment(cursor, answer_id, message, user_id):

    sql_query = """
                INSERT INTO
                comment (answer_id, message, user_id, submission_time, edited_count)
                VALUES (%s, %s, %s, date_trunc('second', now()), 0);
                """

    cursor.execute(sql_query, (answer_id, message, user_id))


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


@connection.connection_handler
def get_user_login_data(cursor, login):

    sql_query = """
                SELECT id, name, password from ask_mate_users
                WHERE name=%(login)s
                """

    cursor.execute(sql_query, {'login': login})
    user_data = cursor.fetchall()

    return user_data


@connection.connection_handler
def get_answers_by_user_name(cursor, user_name):

    sql_query = """
                SELECT message, question_id FROM answer AS a
                JOIN ask_mate_users AS u
                ON a.user_id = u.id
                WHERE u.name = %(user_name)s;
                """

    cursor.execute(sql_query, {'user_name': user_name})

    answer_by_user_name = cursor.fetchall()
    return answer_by_user_name


@connection.connection_handler
def get_questions_by_user_name(cursor, user_name):

    sql_query = """
                SELECT q.id, q.message FROM question as q
                JOIN ask_mate_users AS u
                ON q.user_id = u.id
                WHERE u.name = %(user_name)s;
                """

    cursor.execute(sql_query, {'user_name': user_name})

    question_by_user_name = cursor.fetchall()
    return question_by_user_name


@connection.connection_handler
def get_comments_by_user_name(cursor, user_name):

    sql_query = """
                SELECT c.message, c.question_id FROM comment as c 
                JOIN ask_mate_users AS u
                ON c.user_id = u.id
                WHERE u.name = %(user_name)s;
                """

    cursor.execute(sql_query, {'user_name': user_name})

    comments_by_user_name = cursor.fetchall()
    return comments_by_user_name
