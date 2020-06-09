#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import json
import argparse

from .api import PyEUPI


def main():
    parser = argparse.ArgumentParser(description='Query Phishing Initiative service.')
    parser.add_argument("--url", default='https://phishing-initiative.fr', help='URL where the service is running (no path).')
    parser.add_argument("--key", required=True, help='Authorization key to query the service.')
    parser.add_argument('--debug', action='store_true', help='Enable debug')
    parser.add_argument('--not_verify', default=True, action='store_false', help='Verify SSL certificate')
    parser.add_argument('-f', '--full_text_search', default=False, action='store_true', help='Full text search on a partial URL')
    g = parser.add_mutually_exclusive_group(required=True)
    g.add_argument('-u', '--urls', help='Query a URL. Integer means URL ID, a string search the URL in the database. If 0, it returns the first page of urls.')
    g.add_argument('-s', '--submissions', type=int, help='Query your submissions (if 0, returns the first page of submissions)')
    g.add_argument('-p', '--post', help='URL to submit')
    g.add_argument('-t', '--tag', type=int, help='URL status. 0 = unknown, 1 = phishing, 2 = clean.')
    args = parser.parse_args()

    p = PyEUPI(args.key, args.url, args.not_verify, args.debug)
    if args.urls is not None:
        if args.urls.isdigit():
            uid = int(args.urls)
            if args.urls == 0:
                response = p.get_url('')
            else:
                response = p.get_url(uid)
        elif args.full_text_search:
            response = p.search_url(url=args.urls, order_by='-first_seen')
        else:
            response = p.lookup(url=args.urls)

    elif args.submissions is not None:
        if args.submissions == 0:
            response = p.get_submission('')
        else:
            response = p.get_submission(args.submissions)

    elif args.post is not None:
        response = p.post_submission(args.post)
    elif args.tag is not None:
        response = p.search_url(tag=args.tag, order_by='-first_seen')

    print(json.dumps(response, ensure_ascii=False))
