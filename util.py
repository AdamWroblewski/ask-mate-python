from operator import itemgetter
import data_manager

def sort_by_time_submission(posts):
    return sorted(posts, key=itemgetter('submission_time'), reverse=True)
