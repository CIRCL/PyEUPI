#!/bin/python
# -*- coding: utf-8 -*-

import json
import requests
try:
    from urllib.parse import urljoin
except ImportError:
    from urlparse import urljoin


class PyEUPI(object):

    def __init__(self, auth_token, url='https://fr.dev.phishing-initiative.net'):
        self.url = url

        self.session = requests.Session()
        self.session.headers.update(
            {'Accept': 'application/json',
             'content-type': 'application/json',
             'Authorization': 'Token {}'.format(auth_token)})

    def search_url(self, url):
        path = '/api/v1/urls/?url={}'.format(url)
        response = self.session.get(urljoin(self.url, path), verify=False)
        return response.json()

    def get_url(self, itemid=None):
        path = '/api/v1/urls/'
        if itemid is not None:
            path = '{}{}/'.format(path, itemid)
        response = self.session.get(urljoin(self.url, path), verify=False)
        return response.json()

    def get_submission(self, itemid=None):
        path = '/api/v1/submissions/'
        if itemid is not None:
            path = '{}{}/'.format(path, itemid)
        response = self.session.get(urljoin(self.url, path), verify=False)
        return response.json()

    def post_submission(self, url, comment='', notify=False, tag=0):
        if tag not in [0, 1, 2]:
            raise Exception('Tag can only be in 0 (unknown), 1 (phishing), 2 (clean)')
        query = {'url': url, 'comment': comment, 'notify': notify, 'tag': tag}
        path = '/api/v1/submissions/'
        response = self.session.post(urljoin(self.url, path), verify=False, data=json.dumps(query))
        return response.json()
