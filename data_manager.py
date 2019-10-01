import connection


def get_post_title():
    posts = connection.read_csv_data('sample_data/question.csv')

    title_list = []
    FILE_WITHOUT_HEADERS = 1
    TITLE_INDEX = 4
    for title in posts[FILE_WITHOUT_HEADERS:]:
        title_list.append(title[TITLE_INDEX])

    return title_list
