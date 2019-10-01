import csv


def read_csv_data(file_name):
    with open(file_name) as posts:
        reader = csv.reader(posts)

        file_data = []

        for post in reader:
            file_data.append(post)

        return file_data
