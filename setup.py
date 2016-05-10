#!/usr/bin/env python

from distutils.core import setup

setup(name='CVL Benchmarking',
      version='0.1.0',
      description='Scripts that are needed for Document Analysis benchmarking',
      author='Markus Diem',
      author_email='diem@caa.tuwien.ac.at',
      url='http://www.caa.tuwien.ac.at/cvl/',
      packages=['database', 'writer', 'cvltest'],
      package_dir={'database':  'lib/database',
                   'writer':    'lib/writer',
                   'cvltest':   'lib/cvltest'},
      )

#   package_data={'benchmarking': ['data/*.dat']},
