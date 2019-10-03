import csv


QUESTION_HEADERS = ['id', 'submission_time', 'view_number', 'vote_number', 'title', 'message', 'image']


def read_csv_data(file_name):
    post_list = []
    with open(file_name) as posts:
        reader = csv.DictReader(posts)

        for post in reader:
            post_list.append(post)

    return post_list


def append_csv_data(file_name, data):
    with open(file_name, 'a') as file:
        writer = csv.DictWriter(file, fieldnames=QUESTION_HEADERS)

        writer.writerow(data)
