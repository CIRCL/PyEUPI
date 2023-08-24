.. PyEUPI documentation master file, created by
   sphinx-quickstart on Mon Apr 18 11:08:52 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to PyEUPI's documentation!
==================================

PyEUPI is the Python API Client to query the `Phishing Initiative <https://www.phishing-initiative.eu/>`_ service.

It's used for several purposes, like:

- Submit phishing URLs
- Retrieve your submissions
- Search for content in the URL's source code
- Query information about the URL itself
- Look for an URL qualification


Installation
============

Available for Python3.8+

From the repository:

::

   pip install -e .

Or via pip:

::

   pip install pyeupi

Getting Started !
=================

Create your account
--------------------

Before querying the API, you first need to create your **Phishing Initiative** account.

| France: `phishing-initiative.fr <https://www.phishing-initiative.fr/register>`_
| Luxembourg: `phishing-initiative.lu <https://www.phishing-initiative.lu/register>`_
| Netherlands: `phishing-initiative.nl <https://www.phishing-initiative.nl/register>`_

Get your API key
----------------

Once you've done that, go to `the official API documentation <https://www.phishing-initiative.lu/api/doc/>`_ , there you will find your *rights* and your *API auth key*.

Default users have a limited account. To ask for more rights, you can go to `the contact section <https://www.phishing-initiative.lu/contact/>`_ .

Start Querying !
----------------

::

   from pyeupi import PyEUPI

   p = PyEUPI('Your API key')
   p.search(content='luxembourg')
   p.search_url(tld='lu')
   p.search_submissions(country='Luxembourg')


API Reference
=============

Please refer to `the official API documentation <https://www.phishing-initiative.lu/api/doc/>`_ (or see the :doc:`pyeupi`) to further information on the functions parameters.

.. toctree::
   :maxdepth: 2

   examples.rst
   pyeupi

Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`

