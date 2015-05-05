import os

from setuptools import setup, find_packages


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


setup(name='slugger',
      version='0.2dev',
      description=('Slugging done right. Tries to support close to 300'
                   'languages.'),
      long_description=read('README.rst'),
      keywords='slug slugging web i18n',
      author='Marc Brinkmann',
      author_email='git@marcbrinkmann.de',
      url='http://github.com/mbr/slugger',
      license='LGPLv2.1',
      install_requires=['remember', 'logbook', 'unihandecode'],
      include_package_data=True,
      packages=find_packages(exclude=['glibcparse']),
      classifiers=[
          'Programming Language :: Python :: 2',
          #'Programming Language :: Python :: 3',
      ]
      )
