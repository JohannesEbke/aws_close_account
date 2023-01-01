aws\_close\_account
===================

This is a simple Selenium script to close an AWS account via the web console.
It can also reset the account password, in case it is not known.

*Warning*: This script *does not* ask for further confirmation - it is expressly 
for those that want to skip all those manual steps. So please TAKE CARE and 
uninstall it once you don't need it anymore!

.. image:: https://img.shields.io/pypi/v/aws-close-account
   :alt: PyPI

Why
---
I am creating individual AWS accounts for my students at HM (https://hm.edu)
Closing them at the end of term is boring and annoying, so I automated it.

Also see https://xkcd.com/1319/

Since the AWS Organizations now has the Close Account feature, it seems on first glance
that this script is superfluous. However, closing accounts has some very tight quota
(10% of the active accounts in the organization), so this script unfortunately remains relevant.

Last tested 1st of January 2023.

Requirements / Installation
---------------------------

This program requires an installed selenium driver to run.
It was tested using the selenium driver for firefox 0.30.0 
installed from https://github.com/mozilla/geckodriver/releases .
The selenum driver can be selected with a command line flag.

To install aws-close-account to a virtualenv, do::

  pip install aws-close-account

Usage
-----
The Browser window waits for you to input any captchas and MFA Keys.

Quick Start::

  aws-close-account my-account@example.com
