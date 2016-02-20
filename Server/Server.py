"""
The server side of the restaurant server-client system
"""

# TODO: Cleanup git history
# TODO: Use mock objects for unit testing
# TODO: For all unit tests, use mock objects
# TODO: Code the GUI for Client class
# TODO: ant file to automate Django installation
# TODO: in future, switch to REST API


import http.server
from urllib.parse import urlparse
import django


class Server:

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
        queryDict = dict(query.split("=")
                         for query in parsedURL.query.split("&"))

        # Handles the table database queries
        if parsedURL.path == "/table":
            if queryDict["field"] == "name":
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                self.wfile.write("ABCD-EFGH-IJKL-MNOP".encode("utf-8"))


if __name__ == "__main__":
    server = Server()
    server.server.serve_forever()


