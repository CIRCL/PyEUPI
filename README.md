Client API for EUPI
===================

[![Build Status](https://travis-ci.org/CIRCL/PyEUPI.svg?branch=master)](https://travis-ci.org/CIRCL/PyEUPI)

Client API to query the Phishing Initiative service.

Installation
============

From the repository:

```
    python setup.py install
```

Or via pip:

```
    pip install pyeupi
```

Search queries
==============

```
    from pyeupi import PyEUPI
    p = PyEUPI('<Api key>')
    p.search(content='circl')
    p.search_url(tld='lu')
    p.search_submissions()
```
