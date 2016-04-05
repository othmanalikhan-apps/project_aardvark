"""
A script that allows automation of project management (similar to a MAKEFILE).
"""

#!/usr/bin/env python

from distutils.core import setup

def readme():
    """
    Opens the README file and returns it's contents
    :return: String content of README file
    """
    with open("README.md") as file:
        return file.read()

setup(name='restaurant',
      version='1.0',
      description='Restaurant Booking And Billing System (Client-Server)',
      long_description=readme(),
      classifiers=[
          "License :: :: ",
          "Programming Language :: Python :: 3.4",
          "Topic :: Management :: Restaurant"
      ],
      author='Team Aardvark',
      author_email='sc14omsa@leeds.ac.uk',
      url='https://gitlab.com/comp2541/aardvark',
      packages=['client', "test"],
      install_requires=[
          'requests', 'PyQt5', 'nose'
      ],
      test_suite='tests',
      tests_require=['nose']
     )
