#!/bin/python
# -*- coding: utf-8 -*-

import json
from typing import List, Dict, Any, Optional, Union, Tuple
from urllib.parse import urljoin, urlencode

import requests


class EUPIException(Exception):
    """Catch-all exception for errors emitted by this library."""
    pass


class InvalidSearchQuery(EUPIException):
    """Catch all for all Invalid search query"""
    pass


class PyEUPI(object):

    def __init__(self, auth_token: str, url: str='https://phishing-initiative.eu',
                 verify_ssl: bool=True, debug: bool=False):
        self.url: str = url
        self.debug: bool = debug

        self.session: requests.Session = requests.Session()
        self.session.verify = verify_ssl
        self.session.headers.update({'Accept': 'application/json',
                                     'Authorization': 'Token {}'.format(auth_token)})

    def _get(self, url: str, path: str, query: List=[]) -> Dict[str, Any]:
        to_return: Dict[str, Any] = {}
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
            # If the key doesn't have the rights
            # the API returns a HTML page, normalizing.
            to_return.update({"status": 400,
                              "message": "Probably unauthorized key, enable debug if needed"})
            if self.debug:
                to_return.update({'details': response.text})
                to_return.update({'exception': e})
        return to_return

    def _post(self, url: str, path: str, data: Any) -> Dict[str, Any]:
        to_return: Dict[str, Any] = {}
        full_url = urljoin(url, path)
        if self.debug:
            to_return.update({'url': full_url})
            to_return.update({'query': data})
        response = self.session.post(full_url, data=json.dumps(data), headers={'Content-Type': 'application/json'})
        try:
            to_return.update(response.json())
        except Exception:
            # If the key doesn't have the rights
            # the API returns a HTML page, normalizing.
            to_return.update({"status": 400,
                              "message": "Probably unauthorized key, enable debug if needed"})
            if self.debug:
                to_return.update({'details': response.text})
        return to_return

    def _generic_search_parameters(self, url: Optional[str]=None,
                                   tag: Optional[int]=None,
                                   tag_label: Optional[str]=None,
                                   page: Optional[int]=None,
                                   page_size: Optional[int]=None) -> List[Tuple[str, Union[str, int]]]:
        query: List[Tuple[str, Union[str, int]]] = []
        if page:
            query.append(('page', page))
        if page_size:
            if page_size > 50:
                InvalidSearchQuery('Page size must be <= 50')
            query.append(('page_size', page_size))
        if url:
            query.append(('url', url))
        if tag is not None:
            if tag not in [0, 1, 2]:
                raise InvalidSearchQuery(f'Tag can only be in 0 (unknown), 1 (phishing), 2 (clean) - {tag}')
            query.append(('tag', tag))
        if tag_label:
            labels = ["unknown", "phishing", "clean"]
            if tag_label not in labels:
                raise InvalidSearchQuery('Tag label can only be in {} - {}'.format(', '.join(labels), tag_label))
            query.append(('tag_label', tag_label))
        return query

    def _expanded_search_parameters(self,
                                    tag: Optional[int]=None,
                                    tag_label: Optional[str]=None,
                                    url: Optional[str]=None,
                                    url_exact: Optional[str]=None,
                                    country: Optional[str]=None,
                                    asn: Optional[int]=None,
                                    domain: Optional[str]=None,
                                    redirector: Optional[str]=None,
                                    language: Optional[str]=None,
                                    tld: Optional[str]=None,
                                    ip_address: Optional[str]=None,
                                    ip_range: Optional[str]=None,
                                    first_seen_before: Optional[str]=None,
                                    first_seen_after: Optional[str]=None,
                                    last_tagged_before: Optional[str]=None,
                                    last_tagged_after: Optional[str]=None,
                                    order_by: Optional[str]=None,
                                    page: Optional[int]=None,
                                    page_size: Optional[int]=None) -> List[Tuple[str, Union[str, int]]]:

        query = self._generic_search_parameters(url=url, tag=tag, tag_label=tag_label, page=page, page_size=page_size)
        if url_exact:
            query.append(('url_exact', url_exact))
        if country:
            query.append(('country', country))
        if asn:
            query.append(('asn', asn))
        if domain:
            query.append(('domain', domain))
        if redirector:
            query.append(('redirector', redirector))
        if language:
            query.append(('language', language))
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
        if last_tagged_before:
            query.append(('last_tagged_before', last_tagged_before))
        if last_tagged_after:
            query.append(('last_tagged_after', last_tagged_after))
        if order_by:
            order_opts = ["first_seen", "url", "-first_seen", "-url"]
            if order_by not in order_opts:
                raise InvalidSearchQuery('order_by can only be in {} - {}'.format(', '.join(order_opts), order_by))
            query.append(('order_by', order_by))
        return query

    def search_url(self,
                   tag: Optional[int]=None,
                   tag_label: Optional[str]=None,
                   url: Optional[str]=None,
                   url_exact: Optional[str]=None,
                   country: Optional[str]=None,
                   asn: Optional[int]=None,
                   domain: Optional[str]=None,
                   redirector: Optional[str]=None,
                   language: Optional[str]=None,
                   tld: Optional[str]=None,
                   ip_address: Optional[str]=None,
                   ip_range: Optional[str]=None,
                   first_seen_before: Optional[str]=None,
                   first_seen_after: Optional[str]=None,
                   last_tagged_before: Optional[str]=None,
                   last_tagged_after: Optional[str]=None,
                   order_by: Optional[str]=None,
                   page: Optional[int]=None,
                   page_size: int=50) -> Dict[str, Any]:
        path = '/api/v1/urls/?{}'
        query = self._expanded_search_parameters(
            tag=tag, tag_label=tag_label, url=url, url_exact=url_exact,
            country=country, asn=asn, domain=domain, redirector=redirector, tld=tld,
            language=language, ip_address=ip_address, ip_range=ip_range,
            first_seen_before=first_seen_before,
            first_seen_after=first_seen_after,
            last_tagged_before=last_tagged_before,
            last_tagged_after=last_tagged_after,
            order_by=order_by, page=page, page_size=page_size)
        return self._get(self.url, path, query)

    def get_url(self, itemid: int) -> Dict[str, Any]:
        return self._get(self.url, f'/api/v1/urls/{itemid}/')

    def search(self, url: Optional[str]=None, content: Optional[str]=None,
               tag_label: Optional[str]=None, tag: Optional[int]=None,
               first_seen_after: Optional[str]=None,
               first_seen_before: Optional[str]=None,
               page: Optional[int]=None, page_size: Optional[int]=50) -> Dict[str, Any]:
        path = '/api/v1/urls/search/?{}'
        query = self._generic_search_parameters(url=url, tag=tag, tag_label=tag_label, page=page, page_size=page_size)
        if first_seen_after:
            # TODO: use datetime.isoformat()
            query.append(('first_seen_after', first_seen_after))
        if first_seen_before:
            # TODO: use datetime.isoformat()
            query.append(('first_seen_before', first_seen_before))
        if content:
            query.append(('content', content))
        return self._get(self.url, path, query)

    def lookup(self, url: str) -> Dict[str, Any]:
        return self._get(self.url, '/api/v1/urls/lookup/?{}', [('url', url)])

    # ############# Submissions #############

    def search_submissions(self, submitted_before: Optional[str]=None,
                           submitted_after: Optional[str]=None,
                           order_by: Optional[str]=None,
                           tag: Optional[int]=None,
                           tag_label: Optional[str]=None,
                           url: Optional[str]=None,
                           url_exact: Optional[str]=None,
                           country: Optional[str]=None,
                           asn: Optional[int]=None,
                           domain: Optional[str]=None,
                           redirector: Optional[str]=None,
                           language: Optional[str]=None,
                           tld: Optional[str]=None,
                           ip_address: Optional[str]=None,
                           ip_range: Optional[str]=None,
                           first_seen_before: Optional[str]=None,
                           first_seen_after: Optional[str]=None,
                           last_tagged_before: Optional[str]=None,
                           last_tagged_after: Optional[str]=None,
                           page: Optional[int]=None,
                           page_size: int=50) -> Dict[str, Any]:
        path = '/api/v1/submissions/?{}'
        query = self._expanded_search_parameters(
            tag=tag, tag_label=tag_label, url=url, url_exact=url_exact,
            country=country, asn=asn, domain=domain, redirector=redirector,
            language=language, tld=tld, ip_address=ip_address, ip_range=ip_range,
            first_seen_before=first_seen_before,
            first_seen_after=first_seen_after,
            last_tagged_before=last_tagged_before,
            last_tagged_after=last_tagged_after,
            order_by=order_by, page=page, page_size=page_size)
        if submitted_before:
            query.append(('submitted_before', submitted_before))
        if submitted_after:
            query.append(('submitted_after', submitted_after))
        return self._get(self.url, path, query)

    def get_submission(self, itemid: int) -> Dict[str, Any]:
        return self._get(self.url, f'/api/v1/submissions/{itemid}/')

    def post_submission(self, url: str, comment: str='', notify: bool=False, tag: int=0) -> Dict[str, Any]:
        if tag not in [0, 1, 2]:
            raise Exception(f'Tag can only be in 0 (unknown), 1 (phishing), 2 (clean) - {tag}')
        query = {'url': url, 'comment': comment, 'notify': notify, 'tag': tag}
        path = '/api/v1/submissions/'
        return self._post(self.url, path, query)
