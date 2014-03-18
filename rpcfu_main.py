# "RPCFU", a WSGI compliant application, developed with RPC in mind

#############################################################################
#   Copyright 2012-2014 Hunter Grubbs <hunter.grubbs@gmail.com>
#
#   Licensed under the Apache License, Version 2.0 (the "License");
#   you may not use this file except in compliance with the License.
#   You may obtain a copy of the License at
#
#       http://www.apache.org/licenses/LICENSE-2.0
#
#   Unless required by applicable law or agreed to in writing, software
#   distributed under the License is distributed on an "AS IS" BASIS,
#   WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#   See the License for the specific language governing permissions and
#   limitations under the License.
#############################################################################


def application(environ, start_response):
    import sys
    import datetime
    #import json
    import bson.json_util as json
    from cgi import FieldStorage
    start_time = datetime.datetime.now()  # Grab start time early

    #####################################################################
    ## Set your script_path or imports will fail when deployed via WSGI
    script_path = "/var/www/wsgi/rpcfu/"
    #####################################################################

    if script_path not in sys.path:
        sys.path.append(script_path)  # Set path for WSGI
    from rpcfu_core import RPCMapper  # Import must occur after we append the sys.path if using WSGI

    rpc_handler = RPCMapper.RPCMapper()
    fs_http_args = FieldStorage(fp=environ['wsgi.input'], environ=environ, keep_blank_values=True).list  # get GET/POST
    http_args = dict()  # dict to hold combination of environ & query-string fields
    for arg in fs_http_args:  # copy fieldstorage key:value pairs into http_args
        http_args[arg.name] = arg.value
    for k in environ:  # merge environ with http_args
        if not k.startswith("wsgi"):
            http_args[k] = environ[k]

    rpc_name = environ['PATH_INFO'].replace('/', '', 1)  # Remove leading slash from url

    # Ignore any favicon.ico requests from developers browsing while debugging
    if rpc_name == "favicon.ico":
        status = '200 OK'
        msg = "favicon.ico REQUEST IGNORED"
        response_headers = [('Content-Type', 'application/text'), ('Content-Length', str(len(msg)))]
        start_response(status, response_headers)
        return [msg.encode('utf-8')]

    if rpc_name.startswith("_debug_"):
        rpc_name = rpc_name.replace("_debug_", "")
        send_debug = True
    else:
        send_debug = False
    if 'json_args' in http_args:  # Merge 'json_args' into http_args if present
        #http_args['json_args'] = json.loads(http_args['json_args'].value)
        try:
            decoded_json = json.loads(http_args['json_args'])
        except ValueError:  # invalid JSON handed to us
            http_args['_fatal_error_'] = "invalid JSON provided in json_args"  # Prevent RPC from being attempted
            response_dict = {"error": "JSON provided in json_args unable to be parsed",
                             "original json_args": http_args['json_args']}
            decoded_json = {}  # empty dict() so it can be update()'d into http_args
        http_args.update(decoded_json)
    if '_fatal_error_' not in http_args:
        response_dict = rpc_handler(rpc_name, **http_args)  # Pass RPC name and arguments to handler
    if send_debug is True:
        response_dict['_debug_http'] = http_args
        response_dict['_debug_rpc'] = {
            "rpc_execution_time": (datetime.datetime.now() - start_time).total_seconds(),
        }

    return_status = '200 OK'
    if 'content_type' in response_dict and 'raw_content' in response_dict:  # Handle raw(eg binary/image) replies
        response_headers = [('Content-Type', response_dict['content_type']),
                            ('Content-Length', str(len(response_dict['raw_content'])))]
        if 'content_disposition' in response_dict:
            response_headers.append(('Content-Disposition', response_dict['content_disposition']))
        start_response(return_status, response_headers)
        return [response_dict['raw_content']]
    else:
        response_dict = json.dumps(response_dict)  # encode final response
        response_headers = [('Content-Type', 'application/json'), ('Content-Length', str(len(response_dict)))]
        start_response(return_status, response_headers)
        return [response_dict.encode('utf-8')]

# Start debug_server, or set up path & environ for WSGI deployment if debug_server is False
if __name__ == "__main__":
    debug_server_bind = "0.0.0.0"
    debug_server_port = 8080
    import sys
    try:
        from wsgiref.simple_server import make_server
        print("Creating debug server on %s:%d" % (debug_server_bind, debug_server_port))
        httpd = make_server(debug_server_bind, debug_server_port, application)
        print("Server bound, access the debug server at http://%s:%d/<call_name>" %
              (debug_server_bind, debug_server_port))
        httpd.serve_forever()
    except Exception as e:
        print("Couldn't bind server to %s:%d  - ERROR: %s" % (debug_server_bind, debug_server_port, e))
        sys.exit(1)
