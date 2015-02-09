# "RPCFU", a WSGI compliant application, developed with RPC in mind

#############################################################################
#   Copyright 2012-2014 Hunter Grubbs <hgrubbs@grubbslab.org>
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
    import os
    import json
    import re
    from cgi import FieldStorage

    ##########################################################################
    # Set your script_path first or imports will fail when deployed via WSGI
    script_path = os.path.dirname(os.path.realpath(__file__))
    ##########################################################################

    if script_path not in sys.path:
        sys.path.append(script_path)  # Set path for WSGI
    from models import RPCMapper  # Import must occur after we append the sys.path if using WSGI

    rpc_handler = RPCMapper.ExplicitMapper()
    fs_http_args = FieldStorage(fp=environ['wsgi.input'], environ=environ, keep_blank_values=True).list  # get GET/POST
    http_args = dict()  # dict to hold combination of environ & query-string fields

    # This var must be checked as not being None type. A POST with no data attached will return None from FieldStorage()
    # However, a GET with no data attached will return an iterable with no values.
    if fs_http_args is not None:
        for arg in fs_http_args:  # copy fieldstorage key:value pairs into http_args
            http_args[arg.name] = arg.value
    for k in environ:  # merge environ with http_args
        if not k.startswith("wsgi"):  # skip the wsgi-prefixed data to keep http_args concise
            http_args[k] = environ[k]

    #rpc_name = environ['PATH_INFO'].replace('/', '', 1)  # Remove leading slash from url
    rpc_name = environ['PATH_INFO']
    #rpc_name = re.sub(r'^_*', '', rpc_name)  # remove leading underscores to protect built-ins (ie __class__)

    # Merge 'json_args' into http_args, if 'json_args' is present
    if 'json_args' in http_args:
        try:
            decoded_json = json.loads(http_args['json_args'])
        except ValueError:  # Does the JSON not parse correctly?
            http_args['_fatal_error_'] = "invalid JSON provided in json_args"  # Prevent RPC from being attempted
            response_dict = {"error": "JSON provided in json_args unable to be parsed",
                             "original json_args": http_args['json_args']}
            decoded_json = {}  # empty dict, so it can be update()'d into http_args
        http_args.update(decoded_json)
    if '_fatal_error_' not in http_args:
        response_dict = rpc_handler(rpc_name, **http_args)  # Pass RPC name and arguments to handler


    # Check for specified status codes, otherwise '200 OK'
    if '_status_code' in response_dict:
        status_code = response_dict['_status_code']
        del response_dict['_status_code']
    else:
        status_code = '200'
    if '_status_message' in response_dict:
        status_message = response_dict['_status_message']
        del response_dict['_status_message']
    else:
        status_message = "OK"
    return_status = "%s %s" % (status_code, status_message)

    # Handle return values that return raw data(eg images and other binary data)
    if '_content_type' in response_dict and '_raw_content' in response_dict:
        response_headers = [('Content-Type', response_dict['_content_type']),
                            ('Content-Length', str(len(response_dict['_raw_content']))),
                            ('Access-Control-Allow-Methods', 'POST,GET,PUT'),
                            ('Access-Control-Allow-Origin', '*')
                            ]
        if '_content_disposition' in response_dict:
            response_headers.append(('Content-Disposition', response_dict['_content_disposition']))
        start_response(return_status, response_headers)
        return [response_dict['_raw_content']]

    # Handle return values that return non-binary, non-json replies (eg a HTML view)
    elif '_content_type' in response_dict and '_content' in response_dict:
        response_headers = [('Content-Type', response_dict['_content_type']),
                            ('Content-Length', str(len(response_dict['_content'])))]
        start_response(return_status, response_headers)
        return [response_dict['_content'].encode('utf-8')]

    # Handle all other return values as JSON replies
    else:
        response_dict = json.dumps(response_dict)
        response_headers = [('Content-Type', 'application/json'),
                            ('Content-Length', str(len(response_dict))),
                            ('Access-Control-Allow-Methods', 'POST,GET,PUT'),
                            ('Access-Control-Allow-Origin', '*')
                            ]
        start_response(return_status, response_headers)
        return [response_dict.encode('utf-8')]

# Start debug_server if invoked directly, this is NOT run if loaded by WSGI
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
