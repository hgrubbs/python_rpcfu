from controllers import progress_4gl
from controllers import status
from controllers import tests
from models.auth import AuthError, PermissionError
from models.agility_api.exceptions import AgilityException
import re

# Mappers are defined as classes instead of functions for future functionality - ie separation of map/call steps.


# class ImplicitMapper(object):
#
#     # Override __call__ so we can send requests to the appropriate module and function
#     def __call__(self, url, **args):
#         # URL's appear like 1) /foo/bar or 2) /foo
#         if url.find("/") == -1:  # catches urls like /foo
#             midas_module = None
#             midas_function = url
#         else:  # catches urls like /foo/bar
#             midas_module = url[:url.find("/")]
#             midas_function = url[url.find("/")+1:]
#             # Strip leading underscores, this allows "protected" functions to be defined with an underscore prefix
#             midas_function = re.sub(r'^_*', '', midas_function)
#
#         # Calls individual functions from within defined modules
#         if midas_module == "tests":
#             midas_module = tests
#         elif midas_module == "progress_4gl":
#             midas_module = progress_4gl
#         elif midas_module == "status":
#             midas_module = status
#         elif midas_module is None:  # Module to receive calls when no module is specified
#             midas_module = status
#             if midas_function == '':  # Handle empty URL's, eg http://foo.com/
#                 midas_function = "identify_host"
#
#         try:
#             if hasattr(midas_module, midas_function):
#                 return getattr(midas_module, midas_function)(**args)
#             else:
#                 return {"error": "RPC '%s' does not exist" % url}
#         except TypeError as e:
#                 return {"error": e.args}
#         except AgilityException as e:
#             return {"error": "Agility API replied: %s" % e.value}
#         except AuthError as e:
#             return {"error": "authentication failed", "user": e.value}
#         except PermissionError as e:
#             return {"error": "user does not have permission topic and/or context", "permission": e.value}


class ExplicitMapper(object):

    def __call__(self, url, **args):
        import midas_settings
        import re

        target_function = None

        for url_pattern, url_function in midas_settings.url_map.items():
            m = re.search(url_pattern, url)
            if m is not None:
                args.update(m.groupdict())
                target_function = url_function
                break

        if target_function is None:
            return {"_status_code": 404, "_status_message": "NOT FOUND"}

        try:
            return target_function(**args)
        except TypeError as e:
                return {"error": e.args}
        except AuthError:
            return {"_status_code": 401, "_status_message": "UNAUTHORIZED"}
        except PermissionError:
            return {"_status_code": 401, "_status_message": "UNAUTHORIZED"}
