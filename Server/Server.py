"""
The client side of the restaurant server-client system
"""

import http.server


def runServer():
    serverAddress = ('127.0.0.1', 8000)
    serverClass = http.server.HTTPServer
    handlerClass = http.server.BaseHTTPRequestHandler
    server = serverClass(serverAddress, handlerClass)
    server.serve_forever()


runServer()
