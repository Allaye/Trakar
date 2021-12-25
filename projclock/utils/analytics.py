import operator
from functools import reduce
from datetime import timedelta


def get_total_project_activity_time(activity_data):
    """
    Get total project activity time
    """
    sec_list = [ activity['duration'] for activity in activity_data]
    total_sec = reduce(operator.add, sec_list)
    activities = {
        'total_time': str(timedelta(seconds=round(total_sec.total_seconds()))),
        'user': activity_data[0]['user'],
        'project': activity_data[0]['project'],
    }
    return activities
    