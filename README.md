RPCfu - what is it?
-------------------

RPCfu is a project to create a _very lightweight_ WSGI-compliant RPC framework that speaks JSON. The project is written in Python 3.x, and is the basis for a handful of commercial RPC deployments.

Quick start
-----------
Diving in is easy. Within __rpc_controllers/tests.py__, there are two simple functions defined, and we're going to test them out. Their definitions are:

*  greeter(**request) 
*  personalized_greeter(name, **request) 

To begin, run __rpcfu_main.py__, then visit the URL [http://localhost:8080/tests/greeter](http://localhost:8080/tests/greeter) to see the output of a simple call that takes no inputs.

You should receive this response from your browser:

    {"greeting": "Hello world!"}

Now let's try the somewhat more complex call that takes an input. Visit the URL [http://localhost:8080/tests/personalized_greeter?name=Developer](http://localhost:8080/tests/personalized_greeter?name=Developer).

You should receive this response from your browser:

    {"greeting": "Hello Developer!"}

Simple enough? Both calls have access to the _**request_ dictionary, which contains the WSGI environ. This can be handy to get the client IP, or access multi-part fields sent along with a POST. The *personalized_greeter()*'s argument _name_ should be obvious as well. Positional arguments like _name_ can be added as you see fit, just make sure _**request_ is last in your function definition.

Want some more data about the request and the host? Try changing the name of the controller in the URL from _tests_ to *_debug_tests*. You'll see the environ dumped in the JSON output. This is useful for debugging, but should be disabled in production to avoid giving unnecessary information to clients.

JSON outputs, what about inputs?
--------------------------------
You may supply all inputs via JSON as well, you can even mix and match them. The way to do this is to supply a query string variable named *json_args* containing your arguments. In the _Quick Start_ above, providing `?name=Developer` is the same as providing `{"name": "Developer"}` within the *json_args* variable. Passing arguments as separate query string variables is available mainly for development/debugging, and seems sloppy to deploy in production.

Mapping
-------
Mapping is accomplished in __rpcfu_core/RPCMapper.py__. An example mapping is included that points to __rpc_controllers/test.py__. The quickest introduction to how RPC calls are mapped is to follow the _Quick Start_ above.

Need more documentation?
------------------------
Documentation is (almost) entirely unwritten at this time, but that should be remedied in the near future. If you are interested in helping document the usage of RPCfu, please become a collaborator! Currently, there are a handful of enterprise commercial deployments of RPCfu that extend and take it in wonderful directions. Unfortunately, these deployments are unable to commit their extensions upstream as they contain confidential information about the business. Hopefully these users will sanitize their confidential data and allow these extensions to be shared with the world, but until then feel free to contribute any extensions or improvements you may make.

Use the source Luke!
--------------------
Where documentation may be slim, code comments are not. Code is well commented, and all PEP 8 compliant. Feel free to dive into the (not-so-vast) source code, it's not too terrifying :)
