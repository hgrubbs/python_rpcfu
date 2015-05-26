# Renders jinja2 templated views and returns the proper _content_type and _content for RCPFU to output them


def render(view_file, view_data=None):
    """
    Render a Jinja2 template from view_file and view_data.
    view_file is assumed to be a path relative to views/

    The output is a complete view encapsulated within  dict(_content_type='text/html', _content=<rendered_view>)
    """
    from jinja2 import Template
    import os

    view_file = "%s/../views/%s" % (os.path.dirname(__file__), view_file)  # Pathfix that works for both WSGI and local debugging
    view = open(view_file).read()
    j2_template = Template(view)
    view = j2_template.render(view_data)
    return {"_content_type": "text/html", "_content": view}
