# Test controller, for documentation purposes


def greeter(**request):
    return {"greeting": "Hello world!"}


def personalized_greeter(name, **request):
    return {"greeting": "Hello %s!" % name}
