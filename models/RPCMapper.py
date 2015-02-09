# Mappers are defined as classes instead of functions for future functionality - ie separation of map/call steps.
import rpcfu_settings


class ExplicitMapper(object):

    def __call__(self, url, **args):
        import re

        target_function = None

        for url_pattern, url_function in rpcfu_settings.url_map.items():
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
