#!/usr/bin/env python

from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import traceback

# HTTPRequestHandler class
class ServerModule(BaseHTTPRequestHandler):

    VALID_ROUTE_PREFIX = '/recipes'
    SUCCESS_MESSAGE = json.dumps({"msg": "Success"})
    BAD_REQUEST_MESSAGE = json.dumps({"msg": "Bad Request"})

    # GET
    def do_GET(self):
        result = ServerModule.validate_request(self.path)
        if result[0]:
            recipe_id = result[1]
            if recipe_id is not None:
                print ("Recipe ID : " + str(recipe_id))
            else:
                print ("List of Recipes")
            ServerModule.success(self)
        else:
            ServerModule.bad_request(self)

        return

    # POST
    def do_POST(self):
        self.send_response(200)

        # Send headers
        self.send_header('Content-type','text/html')
        self.end_headers()

        # Send message back to client
        message = self.path
        # Write content as utf-8 data
        self.wfile.write(bytes(message, "utf8"))
        return

    # PUT
    def do_PUT(self):
        self.send_response(200)

        # Send headers
        self.send_header('Content-type','text/html')
        self.end_headers()

        # Send message back to client
        message = self.path
        # Write content as utf-8 data
        self.wfile.write(bytes(message, "utf8"))
        return

    # DELETE
    def do_DELETE(self):
        self.send_response(200)

        # Send headers
        self.send_header('Content-type','text/html')
        self.end_headers()

        # Send message back to client
        message = self.path
        # Write content as utf-8 data
        self.wfile.write(bytes(message, "utf8"))
        return

    @staticmethod
    def validate_request(path):
        if(ServerModule.VALID_ROUTE_PREFIX in path):
            print ("Path : " + path)
            path = path.replace(ServerModule.VALID_ROUTE_PREFIX, '')
            id = path.replace('/','')
            if (len(id) > 0):
                try:
                    id = int(id)
                    return True, id
                except ValueError:
                    print (traceback.format_exc())
                    return False, None
            else:
                return True, None
        else:
            return False, None

    @staticmethod
    def success(req):
        req.send_response(200)
        req.send_header('Content-type','application/json')
        req.end_headers()
        req.wfile.write(bytes(ServerModule.SUCCESS_MESSAGE, "utf8"))
        return req

    @staticmethod
    def bad_request(req):
        req.send_response(400)
        req.send_header('Content-type','application/json')
        req.end_headers()
        req.wfile.write(bytes(ServerModule.BAD_REQUEST_MESSAGE, "utf8"))
        return req


def run():
    print('starting server...')

    # Server settings
    # Choose port 8080, for port 80, which is normally used for a http server, you need root access
    server_address = ('0.0.0.0', 8080)
    httpd = HTTPServer(server_address, ServerModule)
    print('running server...')
    httpd.serve_forever()


run()