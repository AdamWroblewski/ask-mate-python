import csv


def read_csv_data(file_name):
    post_list = []
    with open(file_name) as posts:
        reader = csv.DictReader(posts)

        for post in reader:
            post_list.append(post)

    return post_list
