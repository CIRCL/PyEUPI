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

    def _get(self, url, path, query=[]):
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
                to_return.update({'count': len(r)})
            else:
                to_return.update(r)
        except Exception as e:
            # If the key doesn't have the rights, the API returns a HTML page, normalizing.
            to_return.update({"status": 400, "message": "Probably unauthorized key, enable debug if needed"})
            if self.debug:
                to_return.update({'details': response.text})
                to_return.update({'exception': e})
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

    def _generic_search_parameters(self, url, tag, tag_label, page, page_size):
        query = []
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
        if url:
            query.append(('url', url))
        if tag:
            if tag not in [0, 1, 2]:
                raise Exception('Tag can only be in 0 (unknown), 1 (phishing), 2 (clean)')
            query.append(('tag', tag))
        if tag_label:
            l = ["unknown", "phishing", "clean"]
            if tag_label not in l:
                raise Exception('Tag label can only be in {}'.format(', '.join(l)))
            query.append(('tag_label', tag_label))
        return query

    def _expanded_search_parameters(self, tag, tag_label, url, url_exact, country,
                                    asn, domain, tld, ip_address, ip_range,
                                    first_seen_before, first_seen_after,
                                    order_by, page, page_size):

        query = self._generic_search_parameters(url, tag, tag_label, page, page_size)
        if url_exact:
            query.append(('url_exact', url_exact))
        if country:
            query.append(('country', country))
        if asn:
            query.append(('asn', asn))
        if domain:
            query.append(('domain', domain))
        if tld:
            query.append(('tld', tld))
        if ip_address:
            query.append(('ip_address', ip_address))
        if ip_range:
            query.append(('ip_range', ip_range))
        if first_seen_before:
            query.append(('first_seen_before', first_seen_before))
        if first_seen_after:
            query.append(('first_seen_after', first_seen_after))
        if order_by:
            l = ["first_seen", "url", "-first_seen", "-url"]
            if order_by not in l:
                raise Exception('order_by can only be in {}'.format(', '.join(l)))
            query.append(('order_by', order_by))
        return query

    def search_url(self, tag=None, tag_label=None, url=None, url_exact=None,
                   country=None, asn=None, domain=None, tld=None, ip_address=None,
                   ip_range=None, first_seen_before=None, first_seen_after=None,
                   order_by=None, page=None, page_size=50):
        path = '/api/v1/urls/?{}'
        query = self._expanded_search_parameters(tag, tag_label, url, url_exact,
                                                 country, asn, domain, tld, ip_address,
                                                 ip_range, first_seen_before, first_seen_after,
                                                 order_by, page, page_size)
        return self._get(self.url, path, query)

    def get_url(self, itemid):
        path = '/api/v1/urls/{}/'.format(itemid)
        return self._get(self.url, path)

    def search(self, url=None, content=None, tag_label=None, tag=None, first_seen_since=None,
               first_seen_until=None, page=None, page_size=50):
        path = '/api/v1/urls/search/?{}'
        query = self._generic_search_parameters(url, tag, tag_label, page, page_size)
        if first_seen_since:
            # TODO: use datetime
            query.append(('first_seen_since', first_seen_since))
        if first_seen_until:
            # TODO: use datetime
            query.append(('first_seen_until', first_seen_until))
        if content:
            query.append(('content', content))
        return self._get(self.url, path, query)

    def lookup(self, url):
        path = '/api/v1/urls/lookup/?{}'
        query = [('url', url)]
        return self._get(self.url, path, query)

    # ############# Submissions #############

    def search_submissions(self, submitted_before=None, submitted_after=None,
                           order_by=None, tag=None, tag_label=None, url=None,
                           url_exact=None, country=None, asn=None, domain=None,
                           tld=None, ip_address=None, ip_range=None, page_size=50,
                           first_seen_before=None, first_seen_after=None, page=None):
        path = '/api/v1/submissions/?{}'
        query = self._expanded_search_parameters(tag, tag_label, url, url_exact,
                                                 country, asn, domain, tld, ip_address,
                                                 ip_range, first_seen_before, first_seen_after,
                                                 order_by, page, page_size)
        if submitted_before:
            query.append(('submitted_before', submitted_before))
        if submitted_after:
            query.append(('submitted_after', submitted_after))
        return self._get(self.url, path, query)

    def get_submission(self, itemid):
        path = '/api/v1/submissions/{}/'.format(itemid)
        return self._get(self.url, path)

    def post_submission(self, url, comment='', notify=False, tag=0):
        if tag not in [0, 1, 2]:
            raise Exception('Tag can only be in 0 (unknown), 1 (phishing), 2 (clean)')
        query = {'url': url, 'comment': comment, 'notify': notify, 'tag': tag}
        path = '/api/v1/submissions/'
        return self._post(urljoin(self.url, path), query)
