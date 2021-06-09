#!/usr/bin/env python
# -*- coding: utf-8 -*-
# This is the module's setup script.  To install this module, run:
#
#   python setup.py install
#
import sys
import re

from setuptools import setup, find_packages


VERSION = ""
with open('corpwechat/__init__.py', 'r') as fd:
    VERSION = re.findall("__version__\s*=\s*'([0-9]\.[0-9]\.[0-9]+)'", fd.read())[0]
if not VERSION:
    raise RuntimeError("not found version info")

classifiers = """\
Development Status :: 4 - Beta
Topic :: Utilities
Programming Language :: Python
Programming Language :: Python :: 2.6
Programming Language :: Python :: 2.7
Programming Language :: Python :: 3
Topic :: Software Development :: Libraries :: Python Modules
License :: OSI Approved :: Apache Software License
"""

with open('README.md', 'r') as f:
    doc = f.read()

setup(name='corpwechat',
      version=VERSION,
      author="yorks",
      author_email="yorks.yang@163.com",
      package_dir={ 'corpwechat' : 'corpwechat', },
      packages=['corpwechat'],
      include_package_data=True,
      #py_modules=[''],
      url="https://github.com/yorks/corpwechat",
      download_url = 'https://github.com/yorks/corpwechat/releases/tag/'+VERSION,
      license = "GPLv3.0",
      description=u'a qiye wechat api module, 企业微信的API相关的python实现 https://work.weixin.qq.com/api/doc',
      long_description=doc+'\n\n',
      long_description_content_type='text/markdown',
      platforms = [ "any" ],
      keywords = "api, 企业微信, 微信, wechat, corpwechat",
      classifiers=classifiers.splitlines(),
      install_requires=['requests'],
      #test_suite=unittest.TestSuite,
)

