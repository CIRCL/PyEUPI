.. PyEUPI documentation master file, created by
   sphinx-quickstart on Fri Apr 15 14:10:29 2016.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

:doc:`Back to main page<index>`

URLs database
=============

Browse the Phishing Initiative URLs database.

Query and Retrieve URLs
-----------------------

GET /api/v1/urls/

.. function:: search_url()

   Perform a search on the URL's informations.

   Example:

   ::

      response = p.search_url(tag_label='phishing',
                              first_seen_after='2015-02-01',
			      order_by='first_seen'
			      page_size=15)

Get a specific URL
------------------

GET /api/v1/urls/<int:item_id>/

.. function:: get_url(id)

   Retrieve an URL by its ID.

   Example:

   ::

      response = p.get_url(51325)

Search an URL from its content
------------------------------

GET /api/v1/urls/search/

.. function:: search()

   Search for a string in the URL's source code

   Example:

   ::

      response = p.search(content='Click here',
                          tag=0)


Lookup an URL
-------------

GET /api/v1/urls/lookup/

.. function:: lookup(url)

   Lookup the actual status of an URL.

   Example:

   ::

      response = p.lookup('http://www.paypal.com')


Your submissions
================

Retrieve and Manage your own submissions.

Retrieve submissions
-------------------------

GET /api/v1/submissions/

.. function:: search_submissions()

   Return a list of submissions.

   Example:

   ::

      import datetime

      response = p.search_submissions(first_seen_after='2015-3-15',
                                      tld='com',
                                      asn=16276)

Get a specific submission
-------------------------

GET /api/v1/submissions/<int:item_id>

.. function:: get_submission(id)

   Send back informations about the given submission.

   Example:

   ::

      response = p.get_submission(14527)

Submit an URL
-------------

POST /api/v1/submissions/

.. function:: post_submission(url)

   Submit an URL.

   Example:

   ::

      response = p.post_submission('http://lmpot-france.com/gouv/compte/impots-gouv.fr/file/index.php',
                                   comment='Received a spam today with this link!',
				   notify=True)

