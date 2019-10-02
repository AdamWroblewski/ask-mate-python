import connection
import util


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
            post['id'] = int(post['id'])
            post['submission_time'] = int(post['submission_time'])
            post['view_number'] = int(post['view_number'])
            post['vote_number'] = int(post['vote_number'])
        except ValueError:
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
            util.conver_to_int(answer, 'id', 'submission_time', 'view_number', 'vote_number')
        except ValueError:
            return None

    return answers
