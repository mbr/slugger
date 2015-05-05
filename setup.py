from glob import glob
import os

from setuptools import setup, find_packages
from distutils.command.sdist import sdist


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()


# automatically build the localedata when generating an sdist
class locale_sdist(sdist):
    def run(self):
        if not self.dry_run:
            from slugger.glibcparse.cli import main
            main(glob('glibc/localedata/locales/*'), standalone_mode=False)

        sdist.run(self)


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
      packages=find_packages(exclude=['tests']),
      extras_require = {
          'devtools': ['click'],
      },
      entry_points = {
          'console_scripts': [
              'glcp = slugger.glibcparse.cli:main [devtools]',
          ]
      },
      classifiers=[
          'Programming Language :: Python :: 2',
          #'Programming Language :: Python :: 3',  # no python 3 support yet
      ],
      cmdclass={'sdist': locale_sdist},
      )
