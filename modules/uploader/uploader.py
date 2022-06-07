import datetime
import logging
import os
import random
import string

import PIL
import magic
from PIL import Image
from flask import request, Blueprint, jsonify
from flask_api import status
from pillow_heif import register_heif_opener
from werkzeug.utils import secure_filename

from utils.config import config

uploader_blueprint = Blueprint("uploader_blueprint", __name__)

log = logging.getLogger(__name__)


@uploader_blueprint.route("/upload", methods=["POST"])
def upload():
    if not request.files:
        return "No file part.", status.HTTP_400_BAD_REQUEST

    file = request.files["file"]

    mime_type = get_mime_type(file)
    if not is_mime_allowed(mime_type):
        return "Unsupported media type.", status.HTTP_415_UNSUPPORTED_MEDIA_TYPE

    img_dir = os.path.join(os.getcwd(), "img", datetime.datetime.utcnow().strftime("%Y-%m-%d"))
    if not os.path.exists(img_dir):
        os.mkdir(img_dir)

    try:
        register_heif_opener()
        image = Image.open(file)
        filename = generate_filename(filename=file.filename, extension="webm")
        img_path = os.path.join(img_dir, filename)
        image.save(img_path, format="webp", lossless=True, exif=None)
    except PIL.UnidentifiedImageError:
        filename = generate_filename(file.filename)
        img_path = os.path.join(img_dir, filename)
        file.save(img_path)

    response = {"url": f"{request.host_url}{filename}"}

    return jsonify(response), status.HTTP_200_OK


def get_mime_type(file) -> str:
    file.seek(0)
    mime_type = magic.from_buffer(file.read(2048), mime=True)
    return mime_type


def is_mime_allowed(mime_type: str) -> bool:
    return mime_type.split("/", 1)[0] in config["mime_type"]["allowed"]


def strip_exif(image: Image) -> Image:
    data = list(image.getdata())
    image_without_exif = Image.new(mode=image.mode, size=image.size)
    image_without_exif.putdata(data)
    return image_without_exif


def generate_filename(filename: str, extension: str = None) -> str:
    if not extension:
        extension = filename.rsplit(".", 1)[1]

    if config["random_name"] > 0 or filename == "":
        random_string = "".join(
            random.SystemRandom().choice(string.ascii_letters + string.digits) for _ in range(config["random_name"])
        )
        return f"{random_string}.{extension}"

    return f"{secure_filename(filename).rsplit('.', 1)[0]}.{extension}"
