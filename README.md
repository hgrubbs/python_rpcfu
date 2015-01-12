## RPCfu - what is it? ##

RPCfu is a project to create a _very lightweight_ Python 3x WSGI framework. It receives inputs via query-string field values and/or a single query-string field value containing a JSON.

## Why not Django? Flask? Another WSGI framework? ##

Most popular WSGI frameworks obfuscate how a WSGI transaction takes place. They add in ORM's, complex URL routing rules, mandatory decorators, and other such black magic the programmer is asked to take on good faith. RPCfu does none of these things. Everything happens in two files:, __rcpfu_main.py__ and __RPCMapper.py__. The entire process - from the web request arriving to the result being sent back - can be observed  without following  hundreds of lines of boilerplate code included in large frameworks. In short, by working directly with and understanding this process: _you will become a better programmer_. 

Additionally, RPCfu (for the most part) is a traditional RPC layer, and not another RESTful API. This may or may not be what you are looking for.

## Quick start ##

Diving in is easy. Within __controllers/tests.py__, there are two simple functions defined, and we're going to test them out. Their definitions are:

*  greeter(**request) 
*  personalized_greeter(name, **request) 

To begin, run __rpcfu_main.py__, then visit the URL [http://localhost:8080/tests/greeter](http://localhost:8080/tests/greeter) to see the output of a simple call that takes no inputs.

You should receive this response from your browser:

    {"greeting": "Hello world!"}

Now let's try a call that takes an input. With __rpcfu_main.py__ running, visit the URL [http://localhost:8080/tests/personalized_greeter?name=Developer](http://localhost:8080/tests/personalized_greeter?name=Developer).

You should receive this response from your browser:

    {"greeting": "Hello Developer!"}

Simple enough? Notice how both calls have access to the _**request_ dictionary, which contains the WSGI `environ`. Every call you write should declare _**request_ as the last argument. This can be handy to get the client IP, or access multi-part fields sent along with a POST. The *personalized_greeter()*'s argument _name_ should be self-explanatory as well. Positional arguments like _name_ can be added as you see fit, just make sure _**request_ is last in your function definition.

## Built-in debug server ##

When invoked from the command line, __rpcfu_main.py__ creates a single threaded debug server that listens on port 8080 by default. This should not be used for production, but is handy for debugging. You can use the _pdb_ or _pudb_ python debugging module(and any others you may prefer) to create breakpoints within your application, allowing you to debug in real time from the command line. The debug server is only created when invoked from the command line, and will not exist if called via WSGI.

## JSON inputs? ##

So far you may have noticed that all the inputs have been supplied in URL querystrings, eg `/foo/bar?variable=value`. This is fine, and is also very common. However, if you want to supply everything via JSON, you can. The way to do this is to supply a query string variable named *json_args* containing your arguments in JSON form. In the _Quick Start_ above, providing `?name=Developer` is the same as providing `{"name": "Developer"}` within the *json_args* variable. A URL containing that example in JSON form would appear like `/tests/greeter?json_args=<URL encoded JSON>`. You can pass _both_ query string and json_args provided variables, however values provided in json_args will clobber any query string variables with the same name.

## URL Mapping ##

URL mapping is accomplished in __models/RPCMapper.py__. This is what routes `/tests/greeter` to the file __tests.py__'s function named __greeter(**request)__. An example mapping is included that points to __controllers/tests.py__. The quickest introduction to how RPC calls are mapped is to take a peek inside __RPCMapper.py__ - it's short, concise, and very easy to add to.
