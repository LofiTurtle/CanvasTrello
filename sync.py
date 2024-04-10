import datetime
import json
import traceback

import canvasapi.exceptions
import trello.exceptions

from canvashelper import get_upcoming_assignments
from trellohelper import add_assignments
from secrets import CLASS_LIST_DICT

# Patched version of Trello's fetch_json to fix 403 error
# See https://github.com/sarumont/py-trello/issues/376 for updates on repo maintenance
import trello


def patched_fetch_json(self,
                       uri_path,
                       http_method='GET',
                       headers=None,
                       query_params=None,
                       post_args=None,
                       files=None):
    """ Fetch some JSON from Trello """

    # explicit values here to avoid mutable default values
    if headers is None:
        headers = {}
    if query_params is None:
        query_params = {}
    if post_args is None:
        post_args = {}

    # if files specified, we don't want any data
    data = None
    if files is None and post_args != {}:
        data = json.dumps(post_args)

    # set content type and accept headers to handle JSON
    if http_method in ("POST", "PUT", "DELETE") and not files:
        headers['Content-Type'] = 'application/json; charset=utf-8'

    headers['Accept'] = 'application/json'

    # construct the full URL without query parameters
    if uri_path[0] == '/':
        uri_path = uri_path[1:]
    url = 'https://api.trello.com/1/%s' % uri_path

    if self.oauth is None:
        query_params['key'] = self.api_key
        query_params['token'] = self.api_secret

    # perform the HTTP requests, if possible uses OAuth authentication
    response = self.http_service.request(http_method, url, params=query_params,
                                            headers=headers, data=data,
                                            auth=self.oauth, files=files,
                                            proxies=self.proxies)

    if response.status_code == 401:
        raise trello.Unauthorized("%s at %s" % (response.text, url), response)
    if response.status_code != 200:
        raise trello.ResourceUnavailable("%s at %s" % (response.text, url), response)

    return response.json()


trello.TrelloClient.fetch_json = patched_fetch_json


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
