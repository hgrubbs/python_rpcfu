from controllers import tests as c_tests

url_map = {
    r'^/greeter/{0,1}$': c_tests.greeter,
    r'^/personalized_greeter/{0,1}$': c_tests.personalized_greeter,
    r'^/echo/(?P<arg1>.+)/(?P<arg2>.+)/{0,1}$': c_tests.echo,
}