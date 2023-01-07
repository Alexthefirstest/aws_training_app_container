from flask import request

from source.web import get_metadata
from source.web import main_flask
from source.web import web_constants
from source.web.wrappers import exceptions_handler

_html_page = """<!DOCTYPE html>
<html>
<title>  
Region and zone data
</title>  
<body>
<p>{0} {1}</p>
<br>
<hr>
<br>
<p><a href=/>main page</a></p>
</body>
</html>"""


@main_flask.route(web_constants.REGION_ZONE_LINK, methods=['GET'])
@exceptions_handler
def get_region_and_zone():
    content_to_return = ['region and availability zone', get_metadata.get_region_zone()]

    return {content_to_return[0]: content_to_return[1]} if web_constants.JSON in request.args \
        else _html_page.format(*content_to_return)
