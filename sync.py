import datetime
import traceback

import canvasapi.exceptions
import trello.exceptions

from canvashelper import get_upcoming_assignments
from trellohelper import add_assignments
from secrets import CLASS_LIST_DICT


def main():

    print(f'[{datetime.datetime.now()}] Checking assignments...')

    for class_id in CLASS_LIST_DICT.keys():
        try:
            upcoming_assignments = get_upcoming_assignments(class_id)
            add_assignments(class_id, upcoming_assignments)
        except trello.exceptions.ResourceUnavailable or canvasapi.exceptions.CanvasException as e:
            print(f'Error fetching assignments and updating cards for course: {class_id}')
            traceback.print_exc()


if __name__ == '__main__':
    main()
