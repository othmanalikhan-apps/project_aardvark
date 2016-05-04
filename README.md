## Team Aardvark--Restaurant Booking And Billing System

The project represents a client-server desktop application to be used in restaurants for management purposes.


## Requirements

* Python (3.4)
* Additional Python Libraries (pip installable):
 * requests (2.9.1)
 * Django (1.9.2)
 * Sphinx (1.3.5)
 * model_mommy (1.2.6)
* Additional Python Libraries (not pip installable unfortunately):
 * PyQt5 (http://pyqt.sourceforge.net/Docs/PyQt5/installation.html)

## Key Features

* Booking restaurant tables at some time slot
* Storing and manging the menu
* Handling customer orders
* Handling customer payment


## Running

The project has been largely automated via the setup.py file. In summary, the
 main commands needed can be run directly from command line by entering:

    python setup.py runInstall
    python setup.py runClient (First specify the server socket in settings.ini)
    python setup.py runServer
    python setup.py runTest
    python setup.py runManualTest
    python setup.py runClean
    python setup.py generateDoc
    python setup.py runDoc

For further built-in **bonus** commands by default, seek help via:

    python setup.py --help-commands


## Authors (Team Aardvark)

|                       Name                        |         Email        |   Phone No.  |
| ------------------------------------------------- |:--------------------:| ------------:|
| [Danilo Andrade](https://gitlab.com/u/ed11d2a)    | ed11d2a@leeds.ac.uk  |  07472440699 |
| [Jhighar Mistry](https://gitlab.com/u/sc14jm)     | sc14jm@leeds.ac.uk   |  07472440699 |
| [Othman Ali Khan](https://gitlab.com/u/sc14omsa)  | sc14omsa@leeds.ac.uk |  07472440699 |
| [Pam Iwalewa](https://gitlab.com/u/sc13pi)        | sc13pi@leeds.ac.uk   |  07472440699 |
| [Taiwo Kareem](https://gitlab.com/u/sc14tsk)      | sc14tsk@leeds.ac.uk  |  07472440699 |


## License

This code is distributed under the MIT license. For further information, see the LICENSE file.


## TODO

* Django:
 * Upgrade URL mapping to more formal and proper mappings

* Issue Tracker:
 * Report fixed GUI misalignment bug of description box
