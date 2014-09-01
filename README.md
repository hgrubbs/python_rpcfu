RPCfu - what is it?
-------------------

RPCfu is a project to create a _very lightweight_ WSGI-compliant RPC framework that speaks JSON. The project is written in Python 3.x, and is the basis for a handful of commercial RPC deployments.

Quick start
-----------
Diving in is easy. Within __controllers/tests.py__, there are two simple functions defined, and we're going to test them out. Their definitions are:

*  greeter(**request) 
*  personalized_greeter(name, **request) 

To begin, run __rpcfu_main.py__, then visit the URL [http://localhost:8080/tests/greeter](http://localhost:8080/tests/greeter) to see the output of a simple call that takes no inputs.

You should receive this response from your browser:

    {"greeting": "Hello world!"}

Now let's try a call that takes an input. With __rpcfu_main.py__ running, visit the URL [http://localhost:8080/tests/personalized_greeter?name=Developer](http://localhost:8080/tests/personalized_greeter?name=Developer).

You should receive this response from your browser:

    {"greeting": "Hello Developer!"}

Simple enough? Notice how both calls have access to the _**request_ dictionary, which contains the WSGI environ. Every call you write should declare _**request_ as the last argument. This can be handy to get the client IP, or access multi-part fields sent along with a POST. The *personalized_greeter()*'s argument _name_ should be self-explanatory as well. Positional arguments like _name_ can be added as you see fit, just make sure _**request_ is last in your function definition.

Want some more data about the request and the host? Try changing the name of the controller in the URL from _tests_ to *_debug_tests*. You'll see the environ dumped in the JSON output. This is useful for debugging, but should be disabled in production to avoid giving unnecessary or sensitive information to clients.

Built-in debug server
---------------------
When invoked from the command line, __rpcfu_main.py__ creates a single threaded debug server that listens on port 8080 by default. This should not be used for production, but is handy for debugging. You can use the _pdb_ python debugging module to create breakpoints within your application, allowing you to debug in real time from the command line. The debug server is only created when invoked from the command line, and will not exist if called via WSGI.

JSON output is fine, but what about inputs?
-------------------------------------------
You may supply all inputs via JSON, and even  mix and match them. The way to do this is to supply a query string variable named *json_args* containing your arguments in JSON form. In the _Quick Start_ above, providing `?name=Developer` is the same as providing `{"name": "Developer"}` within the *json_args* variable. Passing arguments as separate query string variables is available mainly for development/debugging, and seems less-than-elegant for production.

Mapping
-------
Mapping is accomplished in __models/RPCMapper.py__. An example mapping is included that points to __controllers/test.py__. The quickest introduction to how RPC calls are mapped is to take a peek inside __RPCMapper.py__ - it's short, concise, and very easy to add to.

Need more documentation?
------------------------
Documentation is (almost) entirely unwritten at this time, but that should be remedied in the near future. If you are interested in helping document the usage of RPCfu, please become a collaborator.

Use the source Luke!
--------------------
Where documentation may be slim, code comments are not. Code is commented, docstrings are (mostly) present, and everything is PEP 8 compliant. Feel free to dive into the code, it's not too terrifying :)
