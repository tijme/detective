.. raw:: html

   <p align="center">

.. image:: https://rawgit.com/tijme/detective/develop/.github/logo.svg?pypi=png.from.svg
   :width: 300px
   :height: 300px
   :alt: Detective logo

.. raw:: html

   <br class="title">
   
.. image:: https://raw.finnwea.com/shield/?firstText=Donate%20via&secondText=Bunq
   :target: https://bunq.me/tijme/0/Raivo;%20a%20native,%20lightweight%20and%20secure%20one-time%20&%20time-based%20password%20client%20built%20for%20iOS
   :alt: Donate via Bunq
   
.. image:: https://raw.finnwea.com/shield/?typeKey=SemverVersion&typeValue1=detective&typeValue2=master
   :target: https://pypi.python.org/pypi/detective/
   :alt: PyPi version

.. image:: https://raw.finnwea.com/shield/?firstText=License&secondText=MIT
   :target: https://github.com/tijme/detective/blob/master/LICENSE.rst
   :alt: License: MIT

.. raw:: html

   </p>
   <h1>Detective</h1>

Detective helps you find information (at your favorite bug bounty program) that you are not supposed to see. It primarily focuses on information disclosure and sensitive data exposure vulnerabilities.

Table of contents
-----------------

-  `Installation <#installation>`__
-  `Usage <#usage>`__
-  `Issues <#issues>`__
-  `License <#license>`__

Installation
------------

First make sure you're on `Python 2.7/3.3 <https://www.python.org/>`__ or higher. Then run the command below to install Detective.

``$ pip install --upgrade detective``

Usage
-------------

**Help**

.. code:: text

   usage: detective [-h] -d DOMAIN [-pmm] [-cos] [-coh] [-cot] [-siv] [-md MAX_DEPTH] [-mt MAX_THREADS]

   required arguments:
      -d DOMAIN, --domain DOMAIN                  the domain to crawl (e.g. https://finnwea.com)

   optional arguments:
      -h, --help                                  show this help message and exit
      -pmm, --protocol-must-match                 only crawl pages with the same protocol as the startpoint (e.g. only https)
      -cos, --crawl-other-subdomains              also crawl pages that have another subdomain than the startpoint
      -coh, --crawl-other-hostnames               also crawl pages that have another hostname than the startpoint
      -cot, --crawl-other-tlds                    also crawl pages that have another tld than the startpoint
      -siv, --stop-if-vulnerable                  stop crawling if a vulnerability was found
      -md MAX_DEPTH, --max-depth MAX_DEPTH        the maximum search depth (default is unlimited)
      -mt MAX_THREADS, --max-threads MAX_THREADS  the maximum amount of simultaneous threads to use (default is 8)

**Example**

``detective -d https://finnwea.com -siv``

Issues
------

Issues or new features can be reported via the GitHub issue tracker. Please make sure your issue or feature has not yet been reported by anyone else before submitting a new one.

License
-------

Detective is open-sourced software licensed under the `MIT license <https://github.com/tijme/detective/blob/master/LICENSE.rst>`__.
