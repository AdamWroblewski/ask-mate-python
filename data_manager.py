import connection


def get_post_title():
    posts = connection.read_csv_data('sample_data/question.csv')

    titles = []
    for post in posts:
        titles.append(post['title'])

    return titles


def get_all_questions():
    return connection.read_csv_data('sample_data/question.csv')


def get_question_by_id(question_id):
    posts = connection.read_csv_data('sample_data/question.csv')

    for post in posts:
        if post['id'] == question_id:
            return post
