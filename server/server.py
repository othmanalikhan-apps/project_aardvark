"""
The server side of the restaurant server-client system
"""

# TODO: Overhaul docstrings

# TODO: Cleanup git history
# TODO: ant file to automate Django installation

# TODO: Code the GUI for Client class

# TODO: Use mock objects for server
# TODO: in future, switch to REST API

# TODO: Ask difference between mock and patch


import http.server
from urllib.parse import urlparse, parse_qs


import django
import os

from os import sys


class Server:
    """
    An HTTP hosted server with an embedded database for the restaurant.
    """

    def __init__(self, serverAddress=("127.0.0.1", 8000)):
        """
        Constructs the server
        """
        serverClass = http.server.HTTPServer
        handlerClass = myHandler
        self.server = serverClass(serverAddress, handlerClass)


class myHandler(http.server.BaseHTTPRequestHandler):
    """
    Responsible for handling incoming client requests.
    """

    def do_GET(self):
        """
        Handles get requests from the client.
        """

        parsedURL = urlparse(self.path)
        queryDict = parse_qs(parsedURL.query)

        # Handles the table database queries
        if parsedURL.path == "/table":
            customer = Booking.objects.get(customer=queryDict["id"][0])

            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(customer.reference_no.encode("utf-8"))


if __name__ == "__main__":
    sys.path.append("../database")
    os.environ["DJANGO_SETTINGS_MODULE"] = "database.settings"
    django.setup()

    from booking.models import Booking

    server = Server()
    server.server.serve_forever()


