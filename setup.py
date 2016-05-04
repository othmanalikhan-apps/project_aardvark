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
import shutil
import webbrowser

import sys
from sys import platform as _platform

from setuptools import setup, find_packages, Command
from setuptools.command.install import install
from setuptools.command.test import test


# Yet to be used. It seems that subprocess.call does not inherit the
# PYTHONPATH variable thus rendering this function useless.
# The alternative solution to solve import issues (although perhaps not
# optimal) is setting all import statements relative to the root directory
# and then calling any script from the project root directory only. This is
# specified by the cwd option in subprocess.call .
def loadPaths():
    """
    Inserts the project paths into system path so that imports and running
    scripts from other scripts does not result in import errors.
    """
    rootPath = os.path.dirname(os.path.abspath(__file__))
    pathList = [os.path.join(rootPath, 'aardvark'),
                os.path.join(rootPath, 'aardvark', 'client')]

    for path in pathList:
        sys.path.append(path)

def readme():
    """
    Opens the README file and returns it's contents
    :return: String content of README file
    """
    with open("README.md") as file:
        return file.read()


class RunClientCommand(Command):
    """
    A command class to runs the client GUI.
    """
    description = "runs client gui"
    # The format is (long option, short option, description).
    user_options = []

    def initialize_options(self):
        """
        Overriding a required abstract method.
        """
        pass

    def finalize_options(self):
        """
        """
        pass

    def run(self):
        """
        Semantically, runs 'python aardvark/client/controller.py' on the
        command line.
        """
        path = os.path.join("aardvark", "client", "controller.py")
        errno = subprocess.call([sys.executable, path])
        if errno != 0:
            raise SystemExit("Unable to run client GUI!")


class RunServerCommand(Command):
    """
    A command class to runs the django server.
    """
    description = "runs django server"
    user_options = []

    def initialize_options(self):
        """
        Overriding a required abstract method.
        """
        pass

    def finalize_options(self):
        """
        """
        pass

    def run(self):
        """
        Semantically, runs 'python aardvark/server/manage.py runserver'
        on the command line.
        """
        path = os.path.join("aardvark", "server", "manage.py")
        errno = subprocess.call([sys.executable, path, "runserver"])
        if errno != 0:
            raise SystemExit("Unable to run the django server!")


class PyTestCommand(test):
    """
    A command class to run tests.
    """
    description = "runs all automatic tests"
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
        Runs both client and django server tests.
        """
        # Not at top level to prevent initial dependency errors
        import pytest

        print("Starting Client Tests:")
        args = ["test"]
        errno1 = pytest.main(args)
        if errno1 != 0:
            raise SystemExit("Unable to run client tests or they failed!")

        print("\n\nStarting Server Tests:")
        serverTestFile = os.path.join(os.getcwd(),
                                      "aardvark", "server", "manage.py")
        errno2 = subprocess.call([sys.executable, serverTestFile, "test"],
                                 cwd=os.path.dirname(serverTestFile))
        if errno2 != 0:
            raise SystemExit("Unable to run server tests or they failed!")


class ManualTestCommand(test):
    """
    A command class to run semi-manual tests.
    """
    description = "runs all manual tests"
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
        Semantically, runs 'python test/manual/gui_test.py' on the
        command line.
        """
        path = os.path.join("test", "manual")
        errno = subprocess.call([sys.executable, "gui_test.py"], cwd=path)
        if errno != 0:
            raise SystemExit("Unable to run manual test!")


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
        ignoreDirs = ["aardvark", "test", "doc", ".git", ".idea", "asset"]
        ignoreFiles = [".gitignore", ".gitlab-ci.yml", "README.md",
                       "setup.py", "settings.ini", "pytest.ini", "LICENSE"]


        deleteDirs = [dir for dir in os.listdir(".")
                      if dir not in ignoreDirs and os.path.isdir(dir)]

        deleteFiles = [file for file in os.listdir(".")
                       if file not in ignoreFiles and os.path.isfile(file)]

        for file in deleteFiles:
            os.remove(file)

        for dir in deleteDirs:
            shutil.rmtree(dir)

        path = os.path.join("doc")
        errno = subprocess.call('make clean', shell=True, cwd=path)
        if errno != 0:
            raise SystemExit("Unable to clean docs!")


class GenerateDocCommand(Command):
    """
    A command class to generate the code documentation.
    """
    description = "generates project documentation"
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
        Generates the project documentation.
        """
        path = os.path.join("doc")
        errno = subprocess.call('make clean && make html', shell=True,
                                cwd=path)
        if errno != 0:
            raise SystemExit("Unable to generate docs!")


class RunDocCommand(Command):
    """
    A command class to open the documentation in the default browser.
    """
    description = "opens documentation in browser"
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
        Opens the project documentation in a browser.
        """
        relativePath = os.path.join("doc", "build", "html", "index.html")
        webbrowser.open('file://' + os.path.realpath(relativePath))


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
            path = os.path.join("venv", "bin", "activate")
            errno2 = subprocess.call('source ' + path, shell=True)

        install.run(self)

        if errno1 != 0:
            raise SystemExit("Unable to setup the virtual environment!")
        if errno2 != 0:
            raise SystemExit("Unable to activate the virtual environment!")


setup(
    name='team_aardvark_restaurant',
    version='1.0',
    packages=find_packages(),

    install_requires=['requests', 'Sphinx', 'Django',
                      'pytest', "model_mommy"],

    cmdclass={
        'runInstall': InstallInVirtualEnv,
        'runClient': RunClientCommand,
        'runServer': RunServerCommand,
        'runTest': PyTestCommand,
        'runManualTest': ManualTestCommand,
        'runClean': CleanCommand,
        'generateDoc': GenerateDocCommand,
        'runDoc': RunDocCommand,
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