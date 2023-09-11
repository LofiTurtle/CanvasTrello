import datetime
from enum import Enum

from trello import TrelloClient, Label
from secrets import TRELLO_API_KEY, TRELLO_API_TOKEN, CANVAS_API_URL, CLASS_LIST_DICT, TRELLO_BOARD_ID, ASSIGNMENT_LABEL_ID
import markdownify


client = TrelloClient(
    api_key=TRELLO_API_KEY,
    api_secret=TRELLO_API_TOKEN
)


class CardLabel(Enum):
    Assignment = Label(client=client, label_id=ASSIGNMENT_LABEL_ID, name="Assignment")


now = datetime.datetime.now()


def format_card_description(course: str, assignment):
    if assignment.description is None:
        assignment.description = ''

    assignment_url = f'{CANVAS_API_URL}courses/{course}/assignments/{assignment.id}'
    # The description field has a 16,384 characters limit
    return f'{assignment_url}\n{markdownify.markdownify(assignment.description)[:16_000 - len(assignment_url)]}`\n\nCard created: {now}`'


def add_assignment_card(course: str, assignment):
    """
    Create card for a canvas assignment
    :param course: The 5 digit canvas course code
    :param assignment: Assignment object returned from canvasapi
    :return: None
    """
    list_id = CLASS_LIST_DICT[course]

    if assignment.description is None:
        assignment.description = ''

    card_desc = format_card_description(course, assignment)
    print(f"[{datetime.datetime.now()}] Creating '{assignment.name}'")

    client.get_list(list_id).add_card(
        name=assignment.name,
        desc=card_desc,
        labels=(CardLabel.Assignment.value,),
        due=assignment.due_at
    )


def add_assignments(course: str, assignments: list, card_filter: str = 'all'):
    trello_cards = client.get_list(CLASS_LIST_DICT[course]).list_cards(card_filter=card_filter)
    for assignment in assignments:
        # Check if assignment is due at midnight (doesn't take DST into account, just checks both PST and PDT)
        if assignment.due_at[-9:-4] == '07:59' or assignment.due_at[-9:-4] == '06:59':
            assignment.due_at = assignment.due_at[:-8] + str(int(assignment.due_at[-8]) - 1) + assignment.due_at[-7:]
            assignment.due_at_date -= datetime.timedelta(hours=1)

        existing_card = next((card for card in trello_cards if card.name == assignment.name), None)
        if existing_card is None:
            add_assignment_card(course, assignment)
        elif existing_card.due[:16] != assignment.due_at[:16]:
            print(f'[{datetime.datetime.now()}] Update due date on {assignment.name} from {existing_card.due} to {assignment.due_at}')
            existing_card.set_due(assignment.due_at_date)
        # check if description has changed. [:-42] is to remove the timestamp before comparing
        elif existing_card.description[:-42] != format_card_description(course, assignment)[:-42]:
            existing_card.set_description(format_card_description(course, assignment))
            print(f'[{datetime.datetime.now()}] Update description on {assignment.name}')


def delete_archived_assignments():
    classes_board = client.get_board(TRELLO_BOARD_ID)
    archived_cards = classes_board.get_cards(card_filter='closed')
    for card in archived_cards:
        print(card.labels)
        if len(card.labels) > 0 and CardLabel.Assignment.value in card.labels:
            card.delete()
    print('archived cards removal complete')

