from flask import request

from source.web import main_flask
from source.web import web_constants

_html_page = """<!DOCTYPE html>
<html>
<title>  
Main page
</title>  
<body>
<p><a href={0}>aws region and availability zone</a></p>
<p><a href={1}>images</a></p>
<p><a href={2}>upload image</a></p>
<p><a href={3}>trigger sqs sns synchro</a></p>
</body>
</html>"""


@main_flask.route('/', methods=['GET'])
@main_flask.route('/index', methods=['GET'])
def get_main_data():
    links_to_return = [web_constants.REGION_ZONE_LINK, web_constants.IMAGES, web_constants.UPLOAD_IMAGE_FORM_LINK,
                       web_constants.TRIGGER_SQS_SNS_SYNC]
    return links_to_return if web_constants.JSON in request.args else _html_page.format(*links_to_return)
