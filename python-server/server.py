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
            if (request_param_hash['valid'] and not request_param_hash['search']):
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
            if(request_param_hash['valid']):
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                input_data = json.loads(post_data.decode("utf-8"))

                if((request_param_hash['id'] is None) and (not request_param_hash['search'])):
                    if (insert(input_data)):
                        ServerModule.success(self)
                    else:
                        ServerModule.bad_request(self)
                elif(request_param_hash['rating'] and (request_param_hash['id'] is not None)):
                    rate_recipe(request_param_hash['id'], input_data)
                    ServerModule.success(self)
                elif(request_param_hash['search']):
                    data = search(input_data)
                    data = json.loads(json_util.dumps(data))
                    ServerModule.success(self, data)
                else:
                    ServerModule.bad_request(self)
            else:
                ServerModule.bad_request(self)
        except:
            print(traceback.format_exc())
            ServerModule.bad_request(self)

        return

    # PUT
    def do_PUT(self):
        request_param_hash = ServerModule.validate_request(self.path)

        try:
            if(request_param_hash['valid'] and (request_param_hash['id'] is not None)):
                content_length = int(self.headers['Content-Length'])
                post_data = self.rfile.read(content_length)
                input_data = json.loads(post_data.decode("utf-8"))

                if (update(request_param_hash['id'], input_data)):
                    ServerModule.success(self)
                else:
                    ServerModule.bad_request(self)
            else:
                ServerModule.bad_request(self)

        except:
            ServerModule.bad_request(self)

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
        search_url_regex = re.compile("/search/recipes")

        is_list_url = list_url_regex.match(path)
        is_id_url = id_url_regex.match(path)
        is_search_url = search_url_regex.match(path)

        path_split = [i for i in path.split("/") if len(i) > 0]

        is_rating_url = 'rating' in path_split
        print (is_rating_url)
        request_param_hash = {"valid": False, "id": None, "rating": False, "search": False}

        if(is_rating_url not in [None, False]):
            id = path_split[1]
            request_param_hash['id'] = id
            request_param_hash['valid'] = True
            request_param_hash['rating'] = True
            request_param_hash['search'] = False
        elif(is_id_url is not None):
            id = path_split[1]
            request_param_hash['id'] = id
            request_param_hash['valid'] = True
            request_param_hash['rating'] = False
            request_param_hash['search'] = False
        elif(is_list_url is not None):
            request_param_hash['id'] = None
            request_param_hash['valid'] = True
            request_param_hash['rating'] = False
            request_param_hash['search'] = False
        elif(is_search_url is not None):
            request_param_hash['id'] = None
            request_param_hash['valid'] = True
            request_param_hash['rating'] = False
            request_param_hash['search'] = True

        print (request_param_hash)
        return request_param_hash            


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