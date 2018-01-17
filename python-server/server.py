#!/usr/bin/env python

from http.server import BaseHTTPRequestHandler, HTTPServer
import re
from bson import json_util
import json
import traceback
from mongo import *

# HTTPRequestHandler class
class ServerModule(BaseHTTPRequestHandler):

    VALID_ROUTE_PREFIX = 'recipes'
    RATINGS_ROUTE_SUFFIX = 'ratings'
    SUCCESS_MESSAGE = {"msg": "Success"}
    BAD_REQUEST_MESSAGE = json.dumps({"msg": "Bad Request"})

    # GET
    def do_GET(self):
        request_param_hash = ServerModule.validate_request(self.path)
        try:
            if (request_param_hash['valid']):
                if(request_param_hash['id'] is not None):
                    ## Get the recipe with id 
                    recipe_json = json.loads(json_util.dumps(get_recipe(request_param_hash['id'])))
                    ServerModule.success(self, recipe_json)
                else:
                    ## Get all recipes
                    all_recipes_json = json.loads(json_util.dumps(list()))
                    ServerModule.success(self, all_recipes_json)
            else:
                ServerModule.bad_request(self)
        except:
            print("Exception while processing the request..")
            print(traceback.format_exc())
            ServerModule.bad_request(self)

        return

    # POST
    def do_POST(self):
        request_param_hash = ServerModule.validate_request(self.path)

        try:
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            input_data = json.loads(post_data.decode("utf-8"))

            if (insert(input_data)):
                ServerModule.success(self)
            else:
                ServerModule.bad_request(self)

        except:
            ServerModule.bad_request(self)

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
        request_param_hash = ServerModule.validate_request(self.path)

        try:
            if (request_param_hash['valid']):
                if(request_param_hash['id'] is not None):
                    id = request_param_hash['id']
                    delete(id)
                    ServerModule.success(self)
                else:
                    ServerModule.bad_request(self)
            else:
                ServerModule.bad_request(self)
        except:
            print(traceback.format_exc())
            ServerModule.bad_request(self)

        return


    @staticmethod
    def validate_request(path):
        list_url_regex = re.compile("/recipes[/]?")
        id_url_regex = re.compile("/recipes/[^()][/]?")
        rating_url_regex = re.compile("/recipes/[^()]/rating[/]?")

        is_list_url = list_url_regex.match(path)
        is_id_url = id_url_regex.match(path)
        is_rating_url = rating_url_regex.match(path)

        path_split = [i for i in path.split("/") if len(i) > 0]

        request_param_hash = {"valid": False, "id": None, "rating": False}

        if(is_rating_url is not None):
            id = path_split[1]
            request_param_hash['valid'] = True
            request_param_hash['id'] = id
            request_param_hash['rating'] = True
        elif(is_id_url is not None):
            id = path_split[1]
            request_param_hash['valid'] = True
            request_param_hash['id'] = id
            request_param_hash['rating'] = False
        elif(is_list_url is not None):
            request_param_hash['valid'] = True
            request_param_hash['id'] = None
            request_param_hash['rating'] = False

        return request_param_hash            


    @staticmethod
    def success(req, content=None):
        req.send_response(200)
        req.send_header('Content-type','application/json')
        req.end_headers()
        response_content = ServerModule.SUCCESS_MESSAGE
        if content is not None:
            response_content['data'] = content
        response_content = json.dumps(response_content)
        req.wfile.write(bytes(response_content, "utf8"))
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