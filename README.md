## Team Aardvark--Restaurant Booking And Billing System

The project represents a client-server desktop application to be used in restaurants for management purposes.

![](assets/demo_splash.png)
![](assets/demo_menu.png)
![](assets/demo_order.png)
![](assets/demo_booking.png)


## Key Features

* Booking restaurant tables at some time slot
* Storing and manging the menu
* Handling customer orders
* Handling customer payment


## Requirements

* Python 3+
  * Django (2.0.2)
  * Sphinx (1.6.3)
  * model-mommy (1.5.1)
  * requests (2.18.4)
  * PyQt5 (5.10.1)


## How to Run

#### Simple Method

Automatically create a local virtual environment and install the necessary
packages into it by running:

    install.bat

Thereafter, launch the server and then connect to it via a client by running:

    runClient.bat
    runServer.bat

#### Fight Me Method

You can manually install the necessary packages thereafter invoking the server
and client via `setup.py`. The full list of commands available are mentioned
below:

    python setup.py runClient
    python setup.py runServer
    python setup.py runTest
    python setup.py runManualTest
    python setup.py runClean
    python setup.py generateDoc
    python setup.py runDoc

For further built-in **bonus** commands by default, seek help via:

    python setup.py --help-commands


## Authors (Team Aardvark)

|                       Name                        |         Email        |
| ------------------------------------------------- |:--------------------:|
| [Othman Ali Khan](https://gitlab.com/u/sc14omsa)  | sc14omsa@leeds.ac.uk |
| [Taiwo Kareem](https://gitlab.com/u/sc14tsk)      | sc14tsk@leeds.ac.uk  |
| [Jhighar Mistry](https://gitlab.com/u/sc14jm)     | sc14jm@leeds.ac.uk   |
| [Danilo Andrade](https://gitlab.com/u/ed11d2a)    | ed11d2a@leeds.ac.uk  |
| [Pam Iwalewa](https://gitlab.com/u/sc13pi)        | sc13pi@leeds.ac.uk   |


## License

This code is distributed under the MIT license. For further information, see the LICENSE file.
