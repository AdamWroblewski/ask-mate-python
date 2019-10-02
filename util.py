from operator import itemgetter
from datetime import datetime


def sort_by_time_submission(posts):
    return sorted(posts, key=itemgetter('submission_time'), reverse=True)


def convert_timestamp_to_date(timestamp):
    return datetime.fromtimestamp(timestamp)


def conver_to_int(dictionary, *args):
    for arg in args:
        if arg not in dictionary.keys():
            raise KeyError('Wrong key.')
        dictionary[arg] = int(dictionary[arg])

