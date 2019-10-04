import connection
import util
from time import time
from operator import itemgetter


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


def get_all_sorted_answers():
    answers = connection.read_csv_data('sample_data/answer.csv')
    for answer in answers:
        try:
            util.conver_to_int(answer, 'id', 'submission_time', 'vote_number', 'question_id')
        except (ValueError, KeyError):
            return None

    answers = sorted(answers, key=itemgetter('submission_time'))

    return answers


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
