# CanvasTrello

CanvasTrello is a tool to populate a Trello board with assignments from Canvas courses. It can be used to manage 
assignments through Trello or view assignments in a calendar using the Calendar plugin from Trello.

## Installation

Clone the repository and run `pip install -r requirements.txt` (tested with Python 3.9), preferably in a virtual 
environment.

## Usage

### Preparing Trello board

This tool only manages cards, and does not manage boards or create lists. You will need to do a few things to get the 
board ready:
1. Create a list for each class you want to sync assignments for
2. Create a new label that you want autopopulated cards to have

### Setting up `secrets.py`

1. Copy `secretstemplate.py` and rename it to `secrets.py`
2. Fill in the fields with your tokens and institution's Canvas URL
3. Fill in the Trello ID fields. You can get IDs by appending `.json` to your Trello board's URL and searching through
the JSON
4. Fill in the Canvas course ID fields. You can get Canvas course IDs by going to your course's homepage and copying 
the numerical ID from the end of the URL

### Running

Run `sync.py` to sync assignments from Canvas to Trello. This is a one-time sync, so you should run this script on a 
schedule to continuously keep the Trello board up-to-date.