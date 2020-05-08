#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from .api import PyEUPI
import json
import argparse


def main():
    parser = argparse.ArgumentParser(description='Query Phishing Initiative service.')
    parser.add_argument("--url", default='https://phishing-initiative.fr', help='URL where the service is running (no path).')
    parser.add_argument("--key", required=True, help='Authorization key to query the service.')
    parser.add_argument('--debug', action='store_true', help='Enable debug')
    parser.add_argument('--not_verify', default=True, action='store_false', help='Verify SSL certificate')
    g = parser.add_mutually_exclusive_group(required=True)
    g.add_argument('-u', '--urls', help='Query a URL. Integer means URL ID, a string search the URL in the database. If 0, it returns the first page of urls.')
    g.add_argument('-s', '--submissions', type=int, help='Query your submissions (if 0, returns the first page of submissions)')
    g.add_argument('-p', '--post', help='URL to submit')
    args = parser.parse_args()

    p = PyEUPI(args.key, args.url, args.not_verify, args.debug)
    if args.urls is not None:
        try:
            uid = int(args.urls)
            if args.urls == 0:
                response = p.get_url('')
            else:
                response = p.get_url(uid)
        except Exception:
            response = p.search_url(args.urls)

    elif args.submissions is not None:
        if args.submissions == 0:
            response = p.get_submission('')
        else:
            response = p.get_submission(args.submissions)

    elif args.post is not None:
        response = p.post_submission(args.post)

    print(json.dumps(response, ensure_ascii=False))
