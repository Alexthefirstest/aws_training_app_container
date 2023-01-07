import base64

from flask import request, redirect
from werkzeug.utils import secure_filename

from source.data_base import images_worker
from source.web import get_metadata
from source.web import main_flask
from source.web import web_constants
from source.web.aws_connectors import s3_connector, sqs_connector
from source.web.wrappers import exceptions_handler

_upload_image_form = """<!DOCTYPE html>
<html>
<title>  
upload image
</title>  
<body>
<form method="post" action="/images" enctype="multipart/form-data">
  <div>
    <label for="file">Choose image to upload </label>
    <input type="file" name="user_image" accept="image/png" />
  </div>
  <div>
  <br>
    <input type="checkbox" name="overwrite"/>
    <label for="overwrite">overwrite if exist</label>
    <br>
  </div>
  <div>
    <button>Submit</button>
  </div>
</form>
<br>
<hr>
<br>
<p><a href=/>main page</a></p>
</body>
</html>"""

_get_images_base = """<!DOCTYPE html>
<html>
<title>  
see images
</title>  
<body>
{0}
<br>
<hr>
<br>
<p><a href=/>main page</a></p>
</body>
</html>"""

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}


def check_and_return_name_extension(filename):
    if '.' not in filename:
        return None
    filename = filename.rsplit('.', 1)
    extension = filename[1]
    return (filename[0], extension) if extension.lower() in ALLOWED_EXTENSIONS else None


@main_flask.route(web_constants.UPLOAD_IMAGE_FORM_LINK, methods=['GET'])
@exceptions_handler
def upload_image_form():
    return _upload_image_form


@main_flask.route(web_constants.IMAGES, methods=['POST'])
@exceptions_handler
def upload_image():
    if 'user_image' not in request.files:
        return ['file not selected']
    file = request.files['user_image']
    if file.filename == '':
        return ['file not selected']
    if not secure_filename(file.filename):
        return ['bad filename']
    file_name_extension = check_and_return_name_extension(file.filename)
    if not file_name_extension:
        return ['wrong file name or extension, available extensions: ', ALLOWED_EXTENSIONS]

    name, ext = file_name_extension
    file_size = len(file.read())
    file.seek(0)

    override = request.form.get('overwrite') == 'on'
    images_worker.add_or_update_image_metadata(name, file_size, ext, override)

    s3_connector.upload_to_s3(file)

    sqs_connector.send_message(
        str({'name': name, 'file_size': file_size, 'extension': ext,
             'link': f'http://{get_metadata.get_public_ip()}{web_constants.IMAGES}/{name}'}))

    return redirect(web_constants.IMAGES + '/' + name)


@main_flask.route(web_constants.IMAGES, methods=['GET'])
@exceptions_handler
def get_images():
    try:
        quantity = request.args.get('quantity')
        st_pos = request.args.get('start_position')

        if quantity:
            quantity = int(quantity)
            if st_pos:
                st_pos = int(st_pos)

        if web_constants.JSON in request.args:
            return images_worker.get_all(quantity, st_pos)
        else:
            return _get_images_base.format(
                ''.join([f'<p><a href={web_constants.IMAGES}/{name}>{name}.{ext}</a> |{size} bites|  |{upd}|</p>'
                         for name, size, ext, upd in images_worker.get_all(quantity, st_pos)]) +
                "<br><p><a href={0}>upload image</a></p>".format(web_constants.UPLOAD_IMAGE_FORM_LINK))

    except ValueError:
        return "quantity and start position should be integer numbers or not added at all"


@main_flask.route(f'{web_constants.IMAGES}/<file_name>', methods=['GET'])
@exceptions_handler
def get_image_by_name(file_name):
    image_data = images_worker.get_one(file_name)
    name, size, ext, upd = image_data
    blob = base64.b64encode(s3_connector.download_from_s3(name, ext))

    if web_constants.JSON in request.args:
        return [*image_data, str(blob)]
    else:
        delete_image_form = \
            f'<form action="{web_constants.IMAGES}/{name}" method="POST"><input type="submit" value="Delete image"/></form>'
        return _get_images_base.format(
            f'<p>{name}.{ext} - {size} bytes, last update date: {upd}</p><br>'
            + f'<img src="data:image/jpg;base64,{str(blob)[2:-1]}"/>'
            + delete_image_form)


@main_flask.route(f'{web_constants.IMAGES}/<name>/metadata', methods=['GET'])
@exceptions_handler
def get_image_metadata_by_name(name):
    if web_constants.JSON in request.args:
        return [images_worker.get_one(name)]
    else:
        name, size, ext, upd = images_worker.get_one(name)
        return _get_images_base.format(f'<p>{name}.{ext} - {size} bytes, last update date: {upd}</p>')


@main_flask.route(f'{web_constants.IMAGES}/<name>', methods=['POST'])
@exceptions_handler
def delete_image_by_name(name):
    extension = images_worker.get_one(name)[2]
    s3_connector.delete_from_s3(name, extension)

    images_worker.delete_raw(name)

    return redirect(web_constants.IMAGES)
