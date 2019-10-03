import connection
import util
from time import time


def get_post_title():
    posts = get_all_questions()

    titles = []
    for post in posts:
        titles.append(post['title'])

    return titles


def get_all_questions():
    posts = connection.read_csv_data('sample_data/question.csv')
    for post in posts:
        try:
            util.conver_to_int(post, 'id', 'submission_time', 'view_number', 'vote_number')
        except (ValueError, KeyError):
            return None

    return posts


def get_question_by_id(question_id):
    posts = get_all_questions()

    for post in posts:
        if post['id'] == question_id:
            return post


def get_all_answers():
    answers = connection.read_csv_data('sample_data/answer.csv')
    for answer in answers:
        try:
            util.conver_to_int(answer, 'id', 'submission_time', 'vote_number', 'question_id')
        except (ValueError, KeyError):
            return None

    return answers


def find_max_question_id():
    questions = connection.read_csv_data('sample_data/question.csv')
    return int(questions[-1]['id'])


def add_new_question(title, msg, img=None):
    question = dict.fromkeys(connection.QUESTION_HEADERS, 0)

    question['id'] = find_max_question_id() + 1
    question['submission_time'] = int(time())
    question['image'] = img
    question['title'] = title
    question['message'] = msg

    connection.append_csv_data('sample_data/question.csv', question)

    return question['id']
