#!/bin/python
# -*- coding: utf-8 -*-

import json
import requests
try:
    from urllib.parse import urljoin, urlencode
except ImportError:
    from urlparse import urljoin
    from urllib import urlencode


class PyEUPI(object):

    def __init__(self, auth_token, url='https://phishing-initiative.fr', verify_ssl=True, debug=False):
        self.url = url
        self.debug = debug

        self.session = requests.Session()
        self.session.verify = verify_ssl
        self.session.headers.update(
            {'Accept': 'application/json',
             'Authorization': 'Token {}'.format(auth_token)})

    def _get(self, url, path, query):
        to_return = {}
        full_url = urljoin(url, path.format(urlencode(query)))
        if self.debug:
            to_return.update({'url': full_url})
        response = self.session.get(full_url)
        try:
            r = response.json()
            if isinstance(r, list):
                # The output if the API isn't consistant
                to_return.update({'results': r})
            else:
                to_return.update(r)
        except Exception as e:
            print e
            # If the key doesn't have the rights, the API returns a HTML page, normalizing.
            to_return.update({"status": 400, "message": "Probably unauthorized key, enable debug if needed"})
            if self.debug:
                to_return.update({'details': response.text})
        return to_return

    def _post(self, url, data):
        to_return = {}
        if self.debug:
            to_return.update({'url': url})
            to_return.update({'query': data})
        response = self.session.post(url, data=json.dumps(data))
        try:
            to_return += response.json()
        except:
            # If the key doesn't have the rights, the API returns a HTML page, normalizing.
            to_return.update({"status": 400, "message": "Probably unauthorized key, enable debug if needed"})
            if self.debug:
                to_return.update({'details': response.text})
        return to_return

    def search_url(self, url):
        path = '/api/v1/urls/?url={}'.format(url)
        return self._get(self.url, path)

    def get_url(self, itemid=None):
        path = '/api/v1/urls/'
        if itemid is not None:
            path = '{}{}/'.format(path, itemid)
        return self._get(self.url, path)

    def get_submission(self, itemid=None):
        path = '/api/v1/submissions/'
        if itemid is not None:
            path = '{}{}/'.format(path, itemid)
        return self._get(self.url, path)

    def lookup(self, url):
        path = '/api/v1/urls/lookup/?{}'
        query = [('url', url)]
        return self._get(self.url, path, query)

    def search(self, url=None, content=None, tag_label=None, tag=None, first_seen_since=None,
               first_seen_until=None, page=None, page_size=None):
        path = '/api/v1/urls/search/?{}'
        query = []
        if url:
            query.append(('url', url))
        if content:
            query.append(('content', content))
        if tag:
            if tag not in [0, 1, 2]:
                raise Exception('Tag can only be in 0 (unknown), 1 (phishing), 2 (clean)')
            query.append(('tag', tag))
        if tag_label:
            l = ["unknown", "phishing", "clean"]
            if tag_label not in l:
                raise Exception('Tag label can only be in {}'.format(', '.join(l)))
            query.append(('tag_label', tag_label))
        if first_seen_since:
            # TODO: use datetime
            query.append(('first_seen_since', first_seen_since))
        if first_seen_until:
            # TODO: use datetime
            query.append(('first_seen_until', first_seen_until))
        if page:
            try:
                page = int(page)
            except:
                raise Exception('Page must be an integer')
            query.append(('page', page))
        if page_size:
            try:
                page_size = int(page_size)
                if page_size > 50:
                    Exception('Page size must be <= 50')
            except:
                raise Exception('Page size must be an integer')
            query.append(('page_size', page_size))
        return self._get(self.url, path, query)

    def post_submission(self, url, comment='', notify=False, tag=0):
        if tag not in [0, 1, 2]:
            raise Exception('Tag can only be in 0 (unknown), 1 (phishing), 2 (clean)')
        query = {'url': url, 'comment': comment, 'notify': notify, 'tag': tag}
        path = '/api/v1/submissions/'
        return self._post(urljoin(self.url, path), query)
