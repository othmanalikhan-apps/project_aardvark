# TODO:
# Add a run server command class
# Add the DEC10 commands for installing PyQT + Django
# Add auto Sphinx autodocumentation
# Report CleanCommand bug that states files are missing when deleting
# Upgrade CleanCommand to remove all files except the chosen ones


"""
A script that allows automated project management (Python's solution to a
MAKEFILE).

The main commands of interest are located within the setup argument,
under cmdclass option.

Also for more details, checkout the README.md file within the project for
further instructions of use.
"""

import os
import subprocess

import sys
from sys import platform as _platform

from setuptools import setup, find_packages, Command
from setuptools.command.install import install


def readme():
    """
    Opens the README file and returns it's contents
    :return: String content of README file
    """
    with open("README.md") as file:
        return file.read()


# def generateCommand(command_subclass):
#     """
#     A decorator method that returns a standard class template for classes
#     that inherit from setuptools command class.
#
#     Specifically, it overrides the abstract methods required for a setuptools
#     command class without adding any functionality.
#     """
#
#     orig_run = command_subclass.run
#     orig_initialize = command_subclass.initialize_options
#     orig_finalize = command_subclass.finalize_options
#
#     def modified_initialize_options(self):
#         """
#         Overrides the empty abstract method.
#
#         The original method is responsible for setting default values for
#         all the options that the command supports.
#
#         In practice, this is used as a lazy constructor.
#         """
# #        orig_initialize(self)
#         pass
#
#     def modified_finalize_options(self):
#         """
#         Overrides the empty abstract method.
#
#         The original method is responsible for setting and checking the final
#         values for all the options just before the method run is executed.
#
#         In practice, this is where the values are assigned and verified.
#         """
# #        orig_finalize(self)
#         pass
#
#     def modified_run(self):
#        """
#        Overrides the default run method but doesn't add any additional
#        functionality yet.
#        """
#        orig_run(self)
#
#    command_subclass.initialize_options = modified_initialize_options
#    command_subclass.finalize_options = modified_finalize_options
#    command_subclass.run = modified_run
#
#    return command_subclass


class RunClientCommand(Command):
    """
    A command class to runs the client GUI.
    """
    description = "runs client gui"
    # The format is (long option, short option, description).
    user_options = [
        ('socket=', None, 'The socket of the server to connect (e.g. '
                          '127.0.0.1:8000'),
    ]

    def initialize_options(self):
        """
        Sets the default value for the server socket.
        """
        self.socket = '127.0.0.1:8000'

    def finalize_options(self):
        """
        Overriding a required abstract method.
        """
        pass

    def run(self):
        """
        Semantically, runs 'python src/client/view.py SERVER_SOCKET' on the
        command line.
        """
        print(self.socket)
        errno = subprocess.call([sys.executable,
                                 'src/client/view.py ' + self.socket])
        if errno != 0:
            raise SystemExit("Unable to run client GUI!")


class PyTestCommand(Command):
    """
    A command class to run tests.
    """
    description = "runs all tests"
    user_options = []

    def initialize_options(self):
        """
        Overriding a required abstract method.
        """
        pass

    def finalize_options(self):
        """
        Overriding a required abstract method.
        """
        pass

    def run(self):
        """
        Semantically, runs 'python test/run_tests.py' on the command line.
        """
        errno = subprocess.call([sys.executable, 'test/run_tests.py'])
        if errno != 0:
            raise SystemExit("Unable to run tests or some tests failed!")


class CleanCommand(Command):
    """
    A command class to clean the current directory (removes folders).
    """
    description = "cleans the project directory"
    user_options = []

    def initialize_options(self):
        """
        Overriding a required abstract method.
        """
        pass

    def finalize_options(self):
        """
        Overriding a required abstract method.
        """
        pass

    def run(self):
        """
        Deletes some folders that can be generated (cross-platform).
        """
        errno = None

        if _platform == "win32":
            errno = subprocess.call('rmdir /s /q build '
                                    'team_aardvark_restaurant.egg-info',
                                    shell=True)

        elif _platform == "linux" or _platform == "linux2":
            errno = subprocess.call('rm -rf build '
                                    'team_aardvark_restaurant.egg-info',
                                    shell=True)

        if errno != 0:
            raise SystemExit("Unable to clean the project directory!")


class InstallInVirtualEnv(install):
    """
    A command class to install the project in a virtual environment
    (cross-platform).
    """

    def run(self):
        """
        Setups up the virtual environment, activates it and then installs the
        project and it's dependencies (cross-platform).
        """
        errno1 = subprocess.call('virtualenv venv', shell=True)

        if _platform == "win32":
            errno2 = subprocess.call('activate', shell=True)

        elif _platform == "linux" or _platform == "linux2":
            errno2 = subprocess.call('source venv/bin/activate', shell=True)

        install.run(self)

        if errno1 != 0:
            raise SystemExit("Unable to setup the virtual environment!")
        if errno1 != 0:
            raise SystemExit("Unable to activate the virtual environment!")


setup(
    name='team_aardvark_restaurant',
    version='1.0',
    packages=find_packages(),

    install_requires=['requests'],
    test_suite="tests",

    cmdclass={
        'runInstallation': InstallInVirtualEnv,
        'runClient': RunClientCommand,
        'runTests': PyTestCommand,
        'runClean': CleanCommand,

    },

    author='Team Aardvark',
    author_email='sc14omsa@leeds.ac.uk',
    description='Restaurant Booking And Billing System (Client-Server)',
    long_description=readme(),
    url='https://gitlab.com/comp2541/aardvark',
    classifiers=[
        "Programming Language :: Python :: 3.4",
        "Topic :: Management :: Restaurant"
    ],
)
