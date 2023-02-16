import datetime

from canvashelper import get_upcoming_assignments
from trellohelper import add_assignments
from secrets import CLASS_LIST_DICT


def main():

    print(f'[{datetime.datetime.now()}] Checking assignments...')

    for class_id in CLASS_LIST_DICT.keys():
        upcoming_assignments = get_upcoming_assignments(class_id)
        add_assignments(class_id, upcoming_assignments)


if __name__ == '__main__':
    main()
