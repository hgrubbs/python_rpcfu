RPCfu - what is it?
-------------------

RPCfu is a project to create a *very lightweight* WSGI-compliant RPC framework. The project is written in Python 3.x, and is the basis for a handful of commercial RPC platforms.

Mapping
-------
Mapping is accomplished in rpcfu_core/RPCMapper.py, and is easily modified for different mapping schemes. The simplest way to get started is to add a new function to the rpc_controllers/test.py module, then fire up the debug server and hit your new function.

Documentation is (almost) entirely unwritten at this time, but that should be remedied in the near future.
