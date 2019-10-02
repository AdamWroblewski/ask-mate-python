import connection


def get_post_title():
    posts = connection.read_csv_data('sample_data/question.csv')

    titles = []
    for post in posts:
        titles.append(post['title'])

    return titles


def get_all_questions():
    return connection.read_csv_data('sample_data/question.csv')
