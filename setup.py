#!/usr/bin/env python
# coding=utf8

import os
import sys

from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(name='slugger',
      version='0.1',
      description="""Slugging done right. Tries to support close to 300
                     languages.""",
      long_description=read('README.rst'),
      keywords='slug slugging web i18n',
      author='Marc Brinkmann',
      author_email='git@marcbrinkmann.de',
      url='http://github.com/mbr/slugger',
      license='LGPL',
      install_requires=['remember', 'logbook', 'unihandecode'],
      include_package_data=True,
      packages=find_packages(exclude=['glibcparse']),
      classifiers=[
          'Development Status :: 4 - Beta',
          'Environment :: Web Environment',
          'Intended Audience :: Developers',
          'License :: OSI Approved :: GNU Library or Lesser General Public License (LGPL)',
          'Operating System :: OS Independent',
          'Topic :: Internet',
          'Topic :: Internet :: WWW/HTTP :: Dynamic Content :: CGI Tools/Libraries',
          'Topic :: Software Development :: Internationalization',
     ]
     )
