from time import time

from psycopg2 import sql

import connection


def get_post_title():
    posts = get_all_questions()

    titles = []
    for post in posts:
        titles.append(post['title'])

    return titles


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


def find_max_id(file_name):
    questions = connection.read_csv_data(file_name)
    return int(questions[-1]['id'])


def add_new_question(title, msg, img=None):
    question_headers = connection.QUESTION_HEADERS
    question = dict.fromkeys(question_headers, 0)

    question['id'] = find_max_id('sample_data/question.csv') + 1
    question['submission_time'] = int(time())
    question['image'] = img
    question['title'] = title
    question['message'] = msg

    connection.append_csv_data('sample_data/question.csv', question, question_headers)

    return question['id']


def add_new_answer(msg, id, img=None):
    answer_headers = connection.ANSWER_HEADERS
    answer = dict.fromkeys(answer_headers, 0)

    answer['id'] = find_max_id('sample_data/answer.csv') + 1
    answer['submission_time'] = int(time())
    answer['message'] = msg
    answer['image'] = img
    answer['question_id'] = id

    connection.append_csv_data('sample_data/answer.csv', answer, answer_headers)
