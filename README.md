Client API for EUPI
===================

[![Build Status](https://travis-ci.org/Rafiot/PyEUPI.svg?branch=master)](https://travis-ci.org/Rafiot/PyEUPI)
[![Documentation Status](https://readthedocs.org/projects/pyeupi/badge/?version=latest)](http://pyeupi.readthedocs.org/en/latest/?badge=latest)

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
