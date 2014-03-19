RPCfu - what is it?
-------------------

RPCfu is a project to create a _very lightweight_ WSGI-compliant RPC framework. The project is written in Python 3.x, and is the basis for a handful of commercial RPC platforms.

Mapping
-------
Mapping is accomplished in __rpcfu_core/RPCMapper.py__. An example mapping is included that points to __rpc_controllers/test.py__.

Quick start
-----------
Within __rpc_controllers/test.py__, there is are two simple functions defined:

*  __greeter(**request)__ 
*  __personalized_greeter(name, **request)__ 

These demonstrate the way new calls are added to RPCfu. Start up __rpcfu_main.py__, then visit the URL [http://localhost:8080/tests/greeter](http://localhost:8080/tests/greeter) to see the output of a simple call that takes no inputs.

You should receive this response from your browser:

    {"greeting": "Hello world!"}

To try a slightly more complex call that takes an input, invoke the __personalized_greeter()__ by visiting the URL [http://localhost:8080/tests/personalized_greeter?name=Developer](http://localhost:8080/tests/personalized_greeter?name=Developer).

You should receive this response from your browser:

    {"greeting": "Hello Developer!"}

Want some more data about the request and the host? Try changing the name of the controller in the URL from _tests_ to _\_debug_tests_, you'll see the environ dumped in the JSON output. This is useful for debugging, but should be disabled in production to avoid giving unnecessary information to clients.

Documentation is (almost) entirely unwritten at this time, but that should be remedied in the near future.
